from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.domain.courses.entities import CourseEntity
    from src.domain.favorite_courses.entities import FavoriteCourseEntity


class AddFavoriteCourseRequest(BaseModel):

    """Schema of new favorite course."""

    course_id: str = Field("05219d1a-e1ef-4c8e-b307-89d41df8ec7b")


class FavoriteCourseDTO(BaseModel):

    """Schema of favorite course."""

    id: str = Field("05219d1a-e1ef-4c8e-b307-89d41df8ec7b")
    course_id: str = Field("05219d1a-e1ef-4c8e-b307-89d41df8ec7b")
    name: str = Field("NoSQL")
    image_url: str | None = Field("image/path-to-file.png")
    implementer: str | None = Field("ИПКН")

    @staticmethod
    def from_domain(course: CourseEntity, favorite_course: FavoriteCourseEntity) -> FavoriteCourseDTO:
        return FavoriteCourseDTO(
            id=favorite_course.id.value,
            course_id=course.id.value,
            name=course.name.value,
            image_url=course.image_url,
            implementer=course.implementer.value if course.implementer else None,
        )
