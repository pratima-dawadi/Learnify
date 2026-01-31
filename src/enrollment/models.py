from django.db import models
from django.utils import timezone
from course.models import Course, Lesson
from user.models import User


class Enrollment(models.Model):
    class Meta:
        db_table = "enrollments"
        unique_together = ("user", "course")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} -> {self.course.title}"

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save(update_fields=["is_completed", "completed_at"])


class LessonProgress(models.Model):
    class Meta:
        db_table = "lesson_progress"
        unique_together = ("enrollment", "lesson")

    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="lesson_progress"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="lesson_progress"
    )
    completed_at = models.DateTimeField(null=True, blank=True)
