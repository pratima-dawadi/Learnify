from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import User


class TestUserRegistration(APITestCase):

    def setUp(self):
        self.register_url = reverse("user-register")

    def test_user_can_register_successfully(self):
        payload = {
            "email": "student1@gmail.com",
            "full_name": "Test Student",
            "password": "strongpassword123",
        }

        response = self.client.post(self.register_url, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "User registered successfully"

        user = User.objects.get(email=payload["email"])
        assert user.full_name == payload["full_name"]
        assert user.check_password(payload["password"])
