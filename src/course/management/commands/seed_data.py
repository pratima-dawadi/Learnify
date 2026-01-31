from django.core.management.base import BaseCommand
from user.models import User, UserRoles
from course.models import Course, Lesson


class Command(BaseCommand):
    help = "Seed the database with instructor, student, courses, and lessons"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding users...")

        # Instructor
        instructor, _ = User.objects.get_or_create(
            email="instructor@gmail.com",
            defaults={
                "full_name": "Instructor",
                "role": UserRoles.INSTRUCTOR,
                "is_staff": True,
            },
        )
        instructor.set_password("instructor123")
        instructor.save()

        # Student
        student, _ = User.objects.get_or_create(
            email="student@gmail.com",
            defaults={
                "full_name": "Student",
                "role": UserRoles.STUDENT,
                "is_staff": False,
            },
        )
        student.set_password("student123")
        student.save()

        self.stdout.write("Seeding courses...")

        courses_data = [
            {
                "title": "Python for Beginners",
                "description": "Learn Python from scratch with hands-on examples.",
                "is_published": True,
            },
            {
                "title": "Django REST Framework",
                "description": "Build powerful REST APIs using Django REST Framework.",
                "is_published": True,
            },
        ]

        courses = []
        for data in courses_data:
            course, _ = Course.objects.get_or_create(
                title=data["title"],
                defaults={
                    "description": data["description"],
                    "is_published": data["is_published"],
                    "user": instructor,
                },
            )
            courses.append(course)

        self.stdout.write("Seeding lessons...")

        lessons_data = [
            {
                "course_index": 0,
                "lessons": [
                    {
                        "title": "Introduction to Python",
                        "content": "Overview of Python and its use cases.",
                        "order": 1,
                    },
                    {
                        "title": "Variables and Data Types",
                        "content": "Learn about variables and basic data types in Python.",
                        "order": 2,
                    },
                ],
            },
            {
                "course_index": 1,
                "lessons": [
                    {
                        "title": "Introduction to DRF",
                        "content": "What is Django REST Framework and why use it?",
                        "order": 1,
                    },
                    {
                        "title": "Serializers in DRF",
                        "content": "Understand serializers and validation in DRF.",
                        "order": 2,
                    },
                ],
            },
        ]

        for course_lessons in lessons_data:
            course = courses[course_lessons["course_index"]]
            for lesson_data in course_lessons["lessons"]:
                Lesson.objects.get_or_create(
                    course=course,
                    title=lesson_data["title"],
                    defaults={
                        "content": lesson_data["content"],
                        "order": lesson_data["order"],
                    },
                )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully!"))
