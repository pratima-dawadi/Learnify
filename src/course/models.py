from django.db import models


class Course(models.Model):
    class Meta:
        db_table = "courses"
        ordering = ["-created_at"]

    title = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "user.User", related_name="courses", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def publish(self):
        self.is_published = True
        self.save()


class Lesson(models.Model):
    class Meta:
        db_table = "lessons"
        ordering = ["order"]

    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
