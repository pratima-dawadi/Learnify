from django.urls import path

from .views import (
    EnrollmentAPIView,
    EnrollmentCompleteAPIView,
    EnrollmentProgressAPIView,
)

urlpatterns = [
    path("enrollments/", EnrollmentAPIView.as_view(), name="enrollments"),
    path(
        "enrollments/<int:pk>/complete/",
        EnrollmentCompleteAPIView.as_view(),
        name="enrollment-complete",
    ),
    path(
        "enrollments/<int:pk>/progress/",
        EnrollmentProgressAPIView.as_view(),
        name="enrollment-progress",
    ),
]
