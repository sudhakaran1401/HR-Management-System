from django.urls import path

from accounts.api.views import CurrentUserAPIView

urlpatterns = [
    path("me/", CurrentUserAPIView.as_view()),
]