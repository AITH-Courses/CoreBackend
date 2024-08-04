from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.domain.courses.entities import CourseEntity



class CourseFullDTO(BaseModel):

    """Schema of course."""

    id: str = Field("423fsdf23ffs3a2sd3432sd2fa2fag")
    name: str = Field("NoSQL")
    image_url: str | None = Field("image/path-to-file.png")
    limits: int | None = Field(25)
    is_draft: bool = Field(default=True)

    prerequisites: str | None = Field("SQL, Basic RDBMS")
    description: str | None = Field("Information about NoSQL")
    topics: str | None = Field("1. History of NoSQL, 2. MongoDB, 3. Cassandra")
    assessment: str | None = Field("The capstone project")
    resources: str | None = Field("1. Book `MongoDB in action`")
    extra: str | None = Field("")

    author: str | None = Field("Иванов И. И.")
    implementer: str | None = Field("ИПКН")
    format: str | None = Field("онлайн-курс")
    terms: str | None = Field("1, 3")
    roles: list[str] = Field(["AI Product Manager"])
    periods: list[str] = Field(["Сентябрь", "Октябрь"])
    last_runs: list[str] = Field(["Весна 2023"])

    @staticmethod
    def from_domain(course: CourseEntity) -> CourseFullDTO:
        return CourseFullDTO(
            id=course.id.value,
            name=course.name.value,
            image_url=course.image_url,
            limits=course.limits,
            is_draft=course.is_draft,

            prerequisites=course.prerequisites,
            description=course.description,
            topics=course.topics,
            assessment=course.assessment,
            resources=course.resources,
            extra=course.extra,

            author=course.author.value if course.author else None,
            implementer=course.implementer.value if course.implementer else None,
            format=course.format.value if course.format else None,
            terms=course.terms.value if course.terms else None,
            roles=[role.value for role in course.roles],
            periods=[period.value for period in course.periods],
            last_runs=[run.value for run in course.last_runs],
        )


class CourseShortDTO(BaseModel):

    """Schema of course in course list."""

    id: str = Field("423fsdf23ffs3a2sd3432sd2fa2fag")
    name: str = Field("NoSQL")
    image_url: str | None = Field("image/path-to-file.png")
    is_draft: bool = Field(default=True)
    implementer: str | None = Field("ИПКН")
    format: str | None = Field("online-курс")
    roles: list[str] = Field(["AI Product Manager"])
    last_runs: list[str] = Field(["Весна 2023"])

    @staticmethod
    def from_domain(course: CourseEntity) -> CourseShortDTO:
        return CourseShortDTO(
            id=course.id.value,
            name=course.name.value,
            image_url=course.image_url,
            is_draft=course.is_draft,
            implementer=course.implementer.value if course.implementer else None,
            format=course.format.value if course.format else None,
            roles=[role.value for role in course.roles],
            last_runs=[run.value for run in course.last_runs],
        )


class CoursesPaginationResponse(BaseModel):

    """Schema of courses pagination."""

    courses: list[CourseShortDTO]
    max_page: int
