from rest_framework.generics import ( CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView )

from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from payroll.models import SalaryHistory
from payroll.services.export_service import ExportService
from .serializers import PayrollSerializer
from rest_framework.views import APIView
from payroll.services.payroll_pdf_service import PayrollPDFService


class PayrollListAPIView(ListAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['employee__first_name', 'employee__last_name']

    ordering_fields = '__all__'

    filterset_fields = ['pay_month']


class PayrollCreateAPIView(CreateAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]


class PayrollDetailAPIView(RetrieveAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]


class PayrollUpdateAPIView(UpdateAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]


class PayrollDeleteAPIView(DestroyAPIView):
    queryset = SalaryHistory.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated]

class PayslipDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        return PayrollPDFService.generate_payslip(pk)
    
class PayrollCSVDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ExportService.generate_salary_csv(request)
    
class PayrollPDFDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return PayrollPDFService.generate_salary_report(request)