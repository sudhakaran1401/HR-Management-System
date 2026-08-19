from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from employees.services.account_service import AccountService
from employees.models import Employee, EmployeeProfile
from employees.services.export_service import ExportService
from employees.services.report_builder_service import EmployeeReportBuilder
from .serializers import EmployeeSerializer
from django.db import transaction

from leave.services.permission_service import PermissionService


def get_employee_for_user(user):
    profile = EmployeeProfile.objects.select_related("employee").filter(user=user).first() 
    return profile.employee if profile and profile.employee else None


class EmployeeManagementPermission(BasePermission):

    message = "Employees cannot manage employee records."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and not PermissionService.employee_only(request.user)
        )


class EmployeeOwnObjectPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not PermissionService.employee_only(request.user):
            return True

        employee = get_employee_for_user(request.user)

        return employee is not None and obj.id == employee.id


class EmployeeCreateAPIView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeManagementPermission]

    @transaction.atomic
    def perform_create(self, serializer):

        employee = serializer.save()

        AccountService.create_account(employee)


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeManagementPermission]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = '__all__'
    filterset_fields = ['department', 'designation']


class EmployeeDetailAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = get_employee_for_user(request.user)

        if employee is None:
            raise PermissionDenied(
                "Employee profile not found for this user."
            )

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)


class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeOwnObjectPermission]


class EmployeeDeleteAPIView(DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeOwnObjectPermission]


class EmployeeReportCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download employee reports."
            )

        month = request.GET.get("month")
        year = request.GET.get("year")

        report = EmployeeReportBuilder.build_joining_report(month, year)

        return ExportService.export_csv(
            report["csv_filename"],
            report["headers"],
            report["rows"],
        )


class EmployeeReportPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download employee reports."
            )

        month = request.GET.get("month")
        year = request.GET.get("year")

        report = EmployeeReportBuilder.build_joining_report(month, year)

        return ExportService.export_pdf(
            report["pdf_filename"],
            month,
            year,
            report["dept_counts"],
            report["headers"],
            report["rows"],
        )
