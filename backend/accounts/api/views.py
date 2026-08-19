from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from employees.models import EmployeeProfile


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        is_hr = False

        try:
            profile = EmployeeProfile.objects.select_related("employee").get(
                user=request.user
            )

            is_hr = profile.employee.department == "HR"

        except EmployeeProfile.DoesNotExist:
            pass

        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "is_hr": is_hr,
        })