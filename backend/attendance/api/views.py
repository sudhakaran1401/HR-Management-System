from rest_framework.generics import ( CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView )
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from attendance.api.serializers import AttendanceSerializer
from attendance.models import Attendance
from attendance.services.attendance_service import AttendanceService
from attendance.services.calendar_service import AttendanceCalendarService
from attendance.services.export_service import AttendanceExportService
from attendance.services.report_service import AttendanceReportService


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


class AttendanceDetailAPIView(RetrieveAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class AttendanceUpdateAPIView(UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


class AttendanceDeleteAPIView(DestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class AttendanceReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
        return AttendanceExportService.generate_csv_response(request)
    
class AttendanceReportPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return AttendanceExportService.generate_pdf_response(request)