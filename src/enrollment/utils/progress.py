from enrollment.models import Enrollment


def calculate_enrollment_progress(enrollment: Enrollment):
    total_lessons = enrollment.course.lessons.count()

    completed_lessons = enrollment.lesson_progress.filter(
        completed_at__isnull=False
    ).count()

    progress = (
        round((completed_lessons / total_lessons) * 100, 2)
        if total_lessons > 0
        else 0.0
    )

    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress": progress,
    }
