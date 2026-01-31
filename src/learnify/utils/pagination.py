from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self: Any, data: Any, extras: Any = None) -> Response:
        return Response(
            {
                "status": "success",
                "message": "Retrieved successfully",
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )
