from rest_framework import serializers
from .models import Course, Lesson


class AddLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["course", "title", "content", "order"]

    def create(self, validated_data):
        lesson = Lesson.objects.create(**validated_data)
        return lesson

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ListLessonSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "content",
            "order",
            "created_at",
            "updated_at",
        ]

    def get_course(self, obj):
        return {
            "id": obj.course.id,
            "title": obj.course.title,
            "description": obj.course.description,
            "is_published": obj.course.is_published,
        }


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "description", "is_published"]

    def create(self, validated_data):
        print(f"Validated data: {validated_data}")
        course = Course.objects.create(**validated_data)
        return course

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ListCourseSerializer(serializers.ModelSerializer):
    lesson_list = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "is_published",
            "created_at",
            "updated_at",
            "lesson_list",
        ]

    def get_lesson_list(self, obj):
        lessons = obj.lessons.all()
        return ListLessonSerializer(lessons, many=True).data
