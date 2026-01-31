from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView

from .filters import CourseFilter, LessonFilter
from .serializers import (
    AddCourseSerializer,
    ListCourseSerializer,
    AddLessonSerializer,
    ListLessonSerializer,
)

from .models import Course, Lesson
from learnify.utils.response import api_response
from learnify.utils.pagination import CustomPagination
from learnify.utils.permission import IsInstructor


class CourseAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsInstructor]
    ordering_fields = ["-updated_at"]
    sort_by = ["-updated_at"]
    paginator = CustomPagination()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsInstructor]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == "instructor":
            return Course.objects.filter(user=user).order_by("-updated_at")
        return Course.objects.filter(is_published=True).order_by("-updated_at")

    @swagger_auto_schema(request_body=AddCourseSerializer)
    def post(
        self: "CourseAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:

        serializer = AddCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user"] = request.user

        serializer.save()

        return api_response(
            data=serializer.data,
            message="Course has been added!",
            status_code=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "is_published",
                openapi.IN_QUERY,
                description="Filter by published status",
                type=openapi.TYPE_BOOLEAN,
            ),
        ]
    )
    def get(
        self: "CourseAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        queryset = self.get_queryset()
        filterset = self.filterset_class(request.GET, queryset=queryset)

        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        queryset = filterset.qs

        page = self.paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = ListCourseSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = ListCourseSerializer(queryset, many=True)
        return api_response(
            data=serializer.data,
            message="List of courses retrieved successfully",
            status_code=status.HTTP_200_OK,
        )


class SpecificCourseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "PATCH":
            self.permission_classes = [IsAuthenticated, IsInstructor]
        return super().get_permissions()

    def get_object(self):
        try:
            if self.request.method == "PATCH":
                return Course.objects.get(id=self.kwargs["id"], user=self.request.user)
            return Course.objects.get(id=self.kwargs["id"])
        except Course.DoesNotExist:
            raise NotFound("Course not found.")

    @swagger_auto_schema(request_body=AddCourseSerializer)
    def patch(
        self: "CourseAPIView", request: Request, id: int, *args: Any, **kwargs: Any
    ) -> Response:
        try:
            course = self.get_object()
        except Course.DoesNotExist:
            raise NotFound("Course not found.")

        serializer = AddCourseSerializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            data=serializer.data,
            message="Course has been updated!",
            status_code=status.HTTP_200_OK,
        )

    def get(self, request, *args, **kwargs):

        try:
            course = self.get_object()
        except Course.DoesNotExist:
            raise NotFound("Course not found.")

        serializer = ListCourseSerializer(course)

        return api_response(
            data=serializer.data,
            message="Course details retrieved successfully",
            status_code=status.HTTP_200_OK,
        )


class LessonAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    paginator = CustomPagination()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated, IsInstructor]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role == "instructor":
            return Lesson.objects.filter(course__user=user)
        return Lesson.objects.filter(course__is_published=True)

    @swagger_auto_schema(request_body=AddLessonSerializer)
    def post(
        self: "LessonAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:

        serializer = AddLessonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            data=serializer.data,
            message="Lesson has been added!",
            status_code=status.HTTP_200_OK,
        )

    @swagger_auto_schema()
    def get(
        self: "LessonAPIView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:

        queryset = self.get_queryset()
        filterset = self.filterset_class(request.GET, queryset=queryset)
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        queryset = filterset.qs

        page = self.paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ListLessonSerializer(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)

        serializer = ListLessonSerializer(queryset, many=True)
        return api_response(
            data=serializer.data,
            message="List of lessons retrieved successfully",
            status_code=status.HTTP_200_OK,
        )


class SpecificLessonAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        try:
            return Lesson.objects.get(
                id=self.kwargs["id"], course__user=self.request.user
            )
        except Lesson.DoesNotExist:
            raise NotFound("Lesson not found.")

    @swagger_auto_schema(request_body=AddLessonSerializer)
    def patch(
        self: "LessonAPIView", request: Request, id: int, *args: Any, **kwargs: Any
    ) -> Response:
        try:
            lesson = self.get_object()
        except Lesson.DoesNotExist:
            raise NotFound("Lesson not found.")

        serializer = AddLessonSerializer(lesson, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            data=serializer.data,
            message="Lesson has been updated!",
            status_code=status.HTTP_200_OK,
        )

    def get(self, request, *args, **kwargs):

        try:
            lesson = self.get_object()
        except Lesson.DoesNotExist:
            raise NotFound("Lesson not found.")

        serializer = ListLessonSerializer(lesson)

        return api_response(
            data=serializer.data,
            message="Lesson details retrieved successfully",
            status_code=status.HTTP_200_OK,
        )
