"""
pagination.py - Reusable pagination utilities for any list endpoint.
"""
from flask import request
from math import ceil


class Paginator:
    """
    Encapsulates pagination logic.
    Usage:
        pager = Paginator(request)
        result = pager.paginate(all_items)
        return result
    """
    MAX_PER_PAGE = 100
    DEFAULT_PER_PAGE = 5

    def __init__(self, req=None):
        self.page = max(1, request.args.get('page', 1, type=int))
        self.per_page = min(
            self.MAX_PER_PAGE,
            request.args.get('per_page', self.DEFAULT_PER_PAGE, type=int)
        )

    def paginate(self, items):
        """Paginate a list and return pagination metadata."""
        total = len(items)
        total_pages = ceil(total / self.per_page) if total > 0 else 0
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        page_items = items[start:end]

        return {
            "data": page_items,
            "pagination": {
                "page": self.page,
                "per_page": self.per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": self.page < total_pages,
                "has_prev": self.page > 1,
                "next_page": self.page + 1 if self.page < total_pages else None,
                "prev_page": self.page - 1 if self.page > 1 else None,
            }
        }
