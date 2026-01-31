from rest_framework import serializers
from .models import Enrollment
from .utils.progress import calculate_enrollment_progress
from course.models import Course, Lesson
from user.models import UserRoles


class EnrollmentSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        request = self.context["request"]
        user = request.user
        try:
            course = Course.objects.get(id=value, is_published=True)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist.")

        if user.role == UserRoles.INSTRUCTOR and course.user_id == user.id:
            raise serializers.ValidationError(
                "Instructors cannot enroll in their own courses."
            )
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        course = Course.objects.get(id=validated_data["course_id"])
        enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)
        if not created:
            raise serializers.ValidationError(
                "User is already enrolled in this course."
            )
        return enrollment


class EnrollmentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "is_published"]


class EnrollmentListSerializer(serializers.ModelSerializer):
    course = EnrollmentCourseSerializer()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "enrolled_at",
            "is_completed",
            "completed_at",
            "progress",
        ]

    def get_progress(self, obj):
        return calculate_enrollment_progress(obj)


class EnrollmentCompleteSerializer(serializers.Serializer):
    lesson = serializers.IntegerField()

    def validate_lesson(self, value):
        enrollment = self.context["enrollment"]

        try:
            lesson = Lesson.objects.get(id=value)

        except Lesson.DoesNotExist:
            raise serializers.ValidationError("Lesson does not exist.")

        if lesson.course_id != enrollment.course_id:
            raise serializers.ValidationError("Lesson does not belong to this course.")

        if enrollment.lesson_progress.filter(
            lesson=lesson,
            completed_at__isnull=False,
        ).exists():
            raise serializers.ValidationError("This lesson has already been completed.")

        # Enforce sequential lesson completion
        completed_count = enrollment.lesson_progress.filter(
            completed_at__isnull=False
        ).count()

        expected_order = completed_count + 1

        if lesson.order != expected_order:
            raise serializers.ValidationError(
                f"You must complete lesson {expected_order} first."
            )

        return lesson
