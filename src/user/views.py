from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserListSerializer,
)
from learnify.utils.response import api_response


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(
        self: "UserRegisterView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return api_response(
            data=serializer.data,
            message="User registered successfully",
            status_code=status.HTTP_201_CREATED,
        )


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(
        self: "UserLoginView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return api_response(
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            message="User logged in successfully",
            status_code=status.HTTP_200_OK,
        )


class UserListView(APIView):

    @swagger_auto_schema()
    def get(
        self: "UserListView", request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        try:
            users = (
                User.objects.all().exclude(is_superuser=True).order_by("-created_at")
            )
            user_data = UserListSerializer(users, many=True).data
            return api_response(
                data=user_data,
                message="User list retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            return api_response(
                message=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserDetailView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = kwargs.get("pk")
        try:
            user = User.objects.get(id=user_id)
            serializer = self.get_serializer(user)
            return api_response(
                data=serializer.data,
                message="User retrieved successfully",
                status_code=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            raise NotFound(detail="User not found")

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = kwargs.get("pk")
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return api_response(
                message="User deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            raise NotFound(detail="User not found")

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user_id = kwargs.get("pk")
        try:
            user = User.objects.get(id=user_id)
            serializer = UserListSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return api_response(
                data=serializer.data,
                message="User updated successfully",
                status_code=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            raise NotFound(detail="User not found")
