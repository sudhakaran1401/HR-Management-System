from django.urls import reverse

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
from rest_framework.views import APIView
from rest_framework.response import Response

from leave.services.approval_service import ApprovalService
from employees.models import Employee
from leave.services.export_service import ExportService
from leave.decorators import get_current_employee
from django.shortcuts import get_object_or_404
from leave.services.balance_service import BalanceService
from leave.models import LeaveRequest
from leave.services.leave_report_builder import LeaveReportBuilder
from .serializers import LeaveRequestSerializer

from leave.services.permission_service import PermissionService


class LeaveOwnObjectPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not PermissionService.employee_only(request.user):
            return True

        current_employee = get_current_employee(request)

        return (
            current_employee is not None
            and obj.employee_id == current_employee.id
        )


class LeaveRequestListAPIView(ListAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['employee__first_name', 'employee__last_name']
    ordering_fields = '__all__'

    filterset_fields = ['status', 'leave_type']


class LeaveRequestCreateAPIView(CreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]


class LeaveRequestDetailAPIView(RetrieveAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]


class LeaveRequestUpdateAPIView(UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]


class LeaveRequestDeleteAPIView(DestroyAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [LeaveOwnObjectPermission]


class LeaveBalanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id=None):

        if PermissionService.employee_only(request.user):
            current_employee = get_current_employee(request)

            # An EMPLOYEE can request only their own balance.
            if employee_id is not None:
                try:
                    requested_employee_id = int(employee_id)
                except (TypeError, ValueError):
                    raise PermissionDenied("Invalid employee ID.")

                if (
                    current_employee is None
                    or requested_employee_id != current_employee.id
                ):
                    raise PermissionDenied(
                        "Employees can only view their own leave balance."
                    )

            employee = current_employee
        else:
            if employee_id:
                employee = get_object_or_404(Employee, id=employee_id)
            else:
                employee = get_current_employee(request)

        if not employee:
            return Response(
                {"error": "Employee profile not linked."},
                status=403,
            )

        balance_data = BalanceService.get_leave_balance(employee)

        data = {
            "employee": str(employee),
            **balance_data,
        }

        return Response(data)


class LeaveApproveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot approve leave requests."
            )

        leave = get_object_or_404(LeaveRequest, pk=pk)

        success, message = ApprovalService.approve_leave(leave)

        if not success:
            return Response({"error": message}, status=400)

        return Response({"message": message}, status=200)


class LeaveRejectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot reject leave requests."
            )

        leave = get_object_or_404(LeaveRequest, pk=pk)

        success, message = ApprovalService.reject_leave(leave)

        if not success:
            return Response({"error": message}, status=400)

        return Response({"message": message}, status=200)


class LeaveReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot access leave reports."
            )

        report = LeaveReportBuilder.build(
            month=request.GET.get("month"),
            year=request.GET.get("year"),
            employee_id=request.GET.get("employee"),
        )

        return Response({
            "summary": report["summary"],
            "headers": report["headers"],
            "rows": report["rows"],
            "employee_name": report["employee_name"],
            "csv_download_url": request.build_absolute_uri(
                reverse("leave_report_download_csv")
            ),
            "pdf_download_url": request.build_absolute_uri(
                reverse("leave_report_download_pdf")
            ),
        })


class LeaveReportCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download leave reports."
            )

        report = LeaveReportBuilder.build(
            month=request.GET.get("month"),
            year=request.GET.get("year"),
            employee_id=request.GET.get("employee"),
        )

        return ExportService.export_csv(
            report["csv_filename"],
            report["headers"],
            report["rows"],
        )


class LeaveReportPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download leave reports."
            )

        report = LeaveReportBuilder.build(
            month=request.GET.get("month"),
            year=request.GET.get("year"),
            employee_id=request.GET.get("employee"),
        )

        return ExportService.export_pdf(
            report["pdf_filename"],
            request.GET.get("month"),
            request.GET.get("year"),
            report["employee_name"],
            report["summary"],
            report["headers"],
            report["rows"],
        )
