from .models import Enrollment

from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from learnify.utils.permission import IsStudent

from .serializers import (
    EnrollmentSerializer,
    EnrollmentListSerializer,
    EnrollmentCompleteSerializer,
)
from learnify.utils.response import api_response
from .models import LessonProgress
from .utils.progress import calculate_enrollment_progress


class EnrollmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=EnrollmentSerializer)
    def post(
        self: "EnrollmentAPIView", request: Request, *args: any, **kwargs: any
    ) -> Response:
        serializer = EnrollmentSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            data=serializer.data,
            message="Enrollment successful!",
            status_code=status.HTTP_200_OK,
        )

    @swagger_auto_schema()
    def get(
        self: "EnrollmentAPIView", request: Request, *args: any, **kwargs: any
    ) -> Response:
        enrollments = Enrollment.objects.filter(user=request.user)
        serializer = EnrollmentListSerializer(enrollments, many=True)

        return api_response(
            data=serializer.data,
            message="Enrollments retrieved successfully!",
            status_code=status.HTTP_200_OK,
        )


class EnrollmentCompleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=EnrollmentCompleteSerializer)
    def patch(
        self: "EnrollmentCompleteAPIView",
        request: Request,
        pk: int,
        *args: any,
        **kwargs: any,
    ) -> Response:
        try:
            enrollment = Enrollment.objects.get(pk=pk, user=request.user)
        except Enrollment.DoesNotExist:
            raise NotFound("Enrollment not found.")

        serializer = EnrollmentCompleteSerializer(
            data=request.data, context={"enrollment": enrollment}
        )
        serializer.is_valid(raise_exception=True)
        lesson = serializer.validated_data["lesson"]

        with transaction.atomic():
            LessonProgress.objects.update_or_create(
                enrollment=enrollment,
                lesson=lesson,
                defaults={"completed_at": timezone.now()},
            )

            # Check if all lessons are completed
            total_lessons = enrollment.course.lessons.count()
            completed_lessons = enrollment.lesson_progress.filter(
                completed_at__isnull=False
            ).count()

            if total_lessons == completed_lessons:
                enrollment.mark_completed()

        return api_response(
            data=None,
            message=f"Lesson '{lesson.title}' marked as completed.",
            status_code=status.HTTP_200_OK,
        )


class EnrollmentProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer

    @swagger_auto_schema()
    def get(
        self: "EnrollmentProgressAPIView",
        request: Request,
        pk: int,
        *args: any,
        **kwargs: any,
    ) -> Response:
        try:
            enrollment = Enrollment.objects.get(pk=pk, user=request.user)
        except Enrollment.DoesNotExist:
            raise NotFound("Enrollment not found.")

        progress_data = calculate_enrollment_progress(enrollment)

        return api_response(
            data=progress_data,
            message="Enrollment progress retrieved successfully!",
            status_code=status.HTTP_200_OK,
        )
