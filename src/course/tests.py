from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from user.models import User
from .models import Course


class TestCourseList(APITestCase):

    def setUp(self):
        # Create student
        self.student = User.objects.create_user(
            email="student@test.com",
            full_name="Test Student",
            password="student123",
            role="student",
        )

        # Create instructor
        self.instructor = User.objects.create_user(
            email="instructor@test.com",
            full_name="Test Instructor",
            password="instructor123",
            role="instructor",
        )

        # Published course
        Course.objects.create(
            title="Published Course",
            description="Visible to students",
            is_published=True,
            user=self.instructor,
        )

        # Unpublished course
        Course.objects.create(
            title="Draft Course",
            description="Hidden from students",
            is_published=False,
            user=self.instructor,
        )

        self.url = reverse("courses")

    def test_student_can_view_only_published_courses(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

        titles = [course["title"] for course in response.data["data"]]

        self.assertIn("Published Course", titles)
        self.assertNotIn("Draft Course", titles)


class TestCourseCreationPermission(APITestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            email="student2@test.com",
            full_name="Student Two",
            password="student123",
            role="student",
        )

        self.url = reverse("courses")

        self.payload = {
            "title": "Illegal Course",
            "description": "Student should not create this",
            "is_published": False,
        }

    def test_student_cannot_create_course(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
