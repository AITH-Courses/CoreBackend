from __future__ import annotations

import math
from typing import Generic, TypeVar

T = TypeVar("T")


class PaginationError(Exception):

    """Base pagination error."""

    @property
    def message(self) -> str:
        return "Some pagination error"


class PageNumberMoreMaxPageError(PaginationError):

    """Error if page > max page."""

    @property
    def message(self) -> str:
        return "This page is more than count of pages"


class PageNumberLessOneError(PaginationError):

    """Error if page < 1."""

    @property
    def message(self) -> str:
        return "This page is less than 1"


class Paginator(Generic[T]):

    """Class for base pagination."""

    def __init__(self, data: list[T], page_size: int) -> None:
        self.n_pages = math.ceil(len(data) / page_size)
        self.page_size = page_size
        self.data = data

    def get_data_by_page(self, page: int) -> list[T]:
        if page > self.n_pages:
            raise PageNumberMoreMaxPageError
        if page < 0:
            raise PageNumberLessOneError
        start_index = (page - 1) * self.page_size
        last_index = page * self.page_size
        return self.data[start_index:last_index]

    @property
    def pages(self) -> list[int]:
        return list(range(1, self.n_pages + 1))
