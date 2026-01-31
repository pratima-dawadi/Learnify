import django_filters

from .models import Course, Lesson


class CourseFilter(django_filters.FilterSet):
    is_published = django_filters.BooleanFilter(field_name="is_published")
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    from_date = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Course
        fields = [
            "is_published",
            "title",
            "from_date",
            "to_date",
        ]


class LessonFilter(django_filters.FilterSet):
    course_id = django_filters.NumberFilter(field_name="course__id")
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    from_date = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Lesson
        fields = [
            "course_id",
            "title",
            "from_date",
            "to_date",
        ]
