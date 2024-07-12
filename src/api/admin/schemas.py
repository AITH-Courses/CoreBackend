from __future__ import annotations

from pydantic import BaseModel, Field


class CreateCourseRequest(BaseModel):

    """Schema of course."""

    name: str = Field("NoSQL")


class CreateCourseResponse(BaseModel):

    """Schema of course."""

    course_id: str = Field("fsf4r6srr6s8f4fs")


class UpdateCourseRequest(BaseModel):

    """Schema of course."""

    name: str = Field("NoSQL")
    image_url: str | None = Field("image/path-to-file.png")
    limits: int | None = Field(25)

    prerequisites: str | None = Field("SQL, Basic RDBMS")
    description: str | None = Field("Information about NoSQL")
    topics: str | None = Field("1. History of NoSQL, 2. MongoDB, 3. Cassandra")
    assessment: str | None = Field("The capstone project")
    resources: str | None = Field("1. Book `MongoDB in action`")
    extra: str | None = Field("")

    author: str | None = Field("Иванов И. И.")
    implementer: str | None = Field("ИПКН")
    format: str | None = Field("online-курс")
    terms: str | None = Field("1, 3")
    roles: list[str] = Field(["AI Product Manager"])
    periods: list[str] = Field(["сентябрь", "октябрь"])
    last_runs: list[str] = Field(["Весна 2023"])
