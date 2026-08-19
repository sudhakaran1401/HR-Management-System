from rest_framework.generics import ( CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView )
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from attendance.api.serializers import AttendanceSerializer
from attendance.models import Attendance
from attendance.services.attendance_service import AttendanceService
from attendance.services.calendar_service import AttendanceCalendarService
from attendance.services.export_service import AttendanceExportService
from attendance.services.report_service import AttendanceReportService
from leave.services.permission_service import PermissionService
from employees.models import EmployeeProfile


def get_employee_for_user(user):
    profile = (
        EmployeeProfile.objects
        .select_related("employee")
        .filter(user=user)
        .first()
    )
    return profile.employee if profile and profile.employee else None


class EmployeeOwnObjectPermission(BasePermission):
   
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not PermissionService.employee_only(request.user):
            return True

        employee = get_employee_for_user(request.user)

        if employee is None:
            return False

        obj_employee_id = getattr(obj, "employee_id", None)

        if obj_employee_id is None:
            obj_employee_id = getattr(obj, "id", None)

        return obj_employee_id == employee.id


class AttendanceListAPIView(ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['employee__first_name', 'employee__last_name']

    ordering_fields = '__all__'

    filterset_fields = ['status', 'date']


class AttendanceCreateAPIView(CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if PermissionService.employee_only(self.request.user):
            employee = serializer.validated_data.get("employee")
            current_employee = get_employee_for_user(self.request.user)

            if (
                current_employee is None
                or employee is None
                or employee.id != current_employee.id
            ):
                raise PermissionDenied(
                    "Employees can only create attendance for themselves."
                )

        serializer.save()


class AttendanceDetailAPIView(RetrieveAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class AttendanceUpdateAPIView(UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [EmployeeOwnObjectPermission]


class AttendanceDeleteAPIView(DestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [EmployeeOwnObjectPermission]


class AttendanceReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download attendance reports."
            )

        data = AttendanceReportService.generate_attendance_report(request)
        return Response(data)


class AttendanceCalendarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = AttendanceService.get_employee_from_user(request.user)
        if not employee:
            return Response([])
        events = AttendanceCalendarService.generate_employee_events(employee)
        return Response(events)


class AttendanceReportCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download attendance reports."
            )

        return AttendanceExportService.generate_csv_response(request)


class AttendanceReportPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if PermissionService.employee_only(request.user):
            raise PermissionDenied(
                "Employees cannot download attendance reports."
            )

        return AttendanceExportService.generate_pdf_response(request)
