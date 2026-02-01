from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from user.models import User
from course.models import Course, Lesson
from .models import Enrollment, LessonProgress


class TestEnrollmentCreation(APITestCase):

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

        # Create a published course
        self.course = Course.objects.create(
            title="Python Basics",
            description="Learn Python from scratch",
            is_published=True,
            user=self.instructor,
        )

        self.url = reverse("enrollments")

    def test_student_cannot_enroll_twice_in_same_course(self):
        self.client.force_authenticate(user=self.student)

        # First enrollment
        Enrollment.objects.create(user=self.student, course=self.course)

        # Attempt second enrollment
        payload = {"course": self.course.id}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify only one enrollment exists
        enrollment_count = Enrollment.objects.filter(
            user=self.student, course=self.course
        ).count()
        self.assertEqual(enrollment_count, 1)


class TestLessonCompletion(APITestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            email="student@test.com",
            full_name="Test Student",
            password="student123",
            role="student",
        )

        self.instructor = User.objects.create_user(
            email="instructor@test.com",
            full_name="Test Instructor",
            password="instructor123",
            role="instructor",
        )

        self.course = Course.objects.create(
            title="Python Course",
            description="Learn Python",
            is_published=True,
            user=self.instructor,
        )

        # Create lessons with sequential order
        self.lesson1 = Lesson.objects.create(
            title="Introduction",
            content="Intro to Python",
            course=self.course,
            order=1,
        )

        self.lesson2 = Lesson.objects.create(
            title="Variables",
            content="Python Variables",
            course=self.course,
            order=2,
        )

        self.lesson3 = Lesson.objects.create(
            title="Functions",
            content="Python Functions",
            course=self.course,
            order=3,
        )

        # Enroll student
        self.enrollment = Enrollment.objects.create(
            user=self.student, course=self.course
        )

    def test_student_cannot_skip_lessons(self):
        self.client.force_authenticate(user=self.student)

        url = reverse("enrollment-complete", kwargs={"pk": self.enrollment.id})

        # Try to complete lesson 2 without completing lesson 1
        payload = {"lesson": self.lesson2.id}

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You must complete lesson 1 first", str(response.data))

        # Verify no progress was created
        self.assertFalse(
            LessonProgress.objects.filter(
                enrollment=self.enrollment, lesson=self.lesson2
            ).exists()
        )

    def test_student_must_complete_lessons_sequentially(self):
        self.client.force_authenticate(user=self.student)

        url = reverse("enrollment-complete", kwargs={"pk": self.enrollment.id})

        # Complete lesson 1
        payload = {"lesson": self.lesson1.id}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to skip to lesson 3
        payload = {"lesson": self.lesson3.id}
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You must complete lesson 2 first", str(response.data))

    def test_student_cannot_complete_same_lesson_twice(self):
        self.client.force_authenticate(user=self.student)

        url = reverse("enrollment-complete", kwargs={"pk": self.enrollment.id})

        # Complete lesson 1 first time
        payload = {"lesson": self.lesson1.id}
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to complete lesson 1 again
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already been completed", str(response.data))
