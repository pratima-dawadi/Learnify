import django_filters

from .models import Enrollment


class EnrollmentFilters(django_filters.FilterSet):
    course_id = django_filters.NumberFilter(field_name="course__id")
    is_completed = django_filters.BooleanFilter(field_name="is_completed")
    from_date = django_filters.DateFilter(field_name="enrolled_at", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="enrolled_at", lookup_expr="lte")

    class Meta:
        model = Enrollment
        fields = [
            "course_id",
            "is_completed",
            "from_date",
            "to_date",
        ]
