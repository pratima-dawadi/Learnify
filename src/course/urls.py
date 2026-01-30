from django.urls import path
from .views import (
    CourseAPIView,
    LessonAPIView,
    SpecificCourseAPIView,
    SpecificLessonAPIView,
)

urlpatterns = [
    path("courses/", CourseAPIView.as_view(), name="courses"),
    path("courses/<int:id>/", SpecificCourseAPIView.as_view(), name="specific_course"),
    path("lessons/", LessonAPIView.as_view(), name="lessons"),
    path("lessons/<int:id>/", SpecificLessonAPIView.as_view(), name="specific_lesson"),
]
