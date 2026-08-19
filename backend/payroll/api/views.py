from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from payroll.models import SalaryHistory
from payroll.services.export_service import ExportService
from .serializers import PayrollSerializer
from rest_framework.views import APIView
from payroll.services.payroll_pdf_service import PayrollPDFService

from employees.models import EmployeeProfile
from leave.services.permission_service import PermissionService


class PayrollManagementPermission(BasePermission):
    """
    Preserve existing behavior for authenticated users who are not in the
    EMPLOYEE group, while blocking EMPLOYEE users from payroll management.
    """

    message = "Employees cannot manage payroll records."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and not PermissionService.employee_only(request.user)
        )


def get_employee_for_user(user):
    profile = (
        EmployeeProfile.objects
        .select_related("employee")
        .filter(user=user)
        .first()
    )
    return profile.employee if profile and profile.employee else None


class PayrollListAPIView(ListAPIView):
    serializer_class = PayrollSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = ["pay_month"]
    ordering_fields = "__all__"
    filterset_fields = ["pay_month"]

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # HR/Admin → all payroll records
        if PermissionService.hr_or_admin(user):
            return SalaryHistory.objects.all()

        # Employee → only their own payroll records
        employee = getattr(
            getattr(user, "employee_profile", None),
            "employee",
            None,
        )

        if employee is None:
            return SalaryHistory.objects.none()

        return SalaryHistory.objects.filter(
            employee=employee
        )


class PayrollCreateAPIView(CreateAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [PayrollManagementPermission]


class PayrollDetailAPIView(RetrieveAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]


class PayrollUpdateAPIView(UpdateAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [PayrollManagementPermission]


class PayrollDeleteAPIView(DestroyAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [PayrollManagementPermission]


class PayslipDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        salary = SalaryHistory.objects.filter(pk=pk).first()

        if salary is None:
            # Preserve the existing service behavior for missing records.
            return PayrollPDFService.generate_payslip(pk)

        if PermissionService.employee_only(request.user):
            employee = get_employee_for_user(request.user)

            if employee is None or salary.employee_id != employee.id:
                raise PermissionDenied(
                    "Employees can only download their own payslip."
                )

        return PayrollPDFService.generate_payslip(pk)


class PayrollCSVDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download payroll reports."
            )

        return ExportService.generate_salary_csv(request)


class PayrollPDFDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download payroll reports."
            )

        return PayrollPDFService.generate_salary_report(request)
