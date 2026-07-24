from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from employees.services.account_service import AccountService
from employees.models import Employee
from employees.services.export_service import ExportService
from employees.services.report_builder_service import EmployeeReportBuilder
from .serializers import EmployeeSerializer
from django.db import transaction


class EmployeeCreateAPIView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):

        employee = serializer.save()

        AccountService.create_account(employee)


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

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
        serializer = EmployeeSerializer(request.user.employee)
        return Response(serializer.data)


class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class EmployeeDeleteAPIView(DestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class EmployeeReportCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
    