from pydantic import BaseModel

from src.domain.course_run.entities import CourseRunEntity


class CreateCourseRunRequest(BaseModel):

    """Schema of create course run request."""

    season: str
    year: int


class CreateCourseRunResponse(BaseModel):

    """Schema of create course run response."""

    course_run_id: str


class CourseRunDTO(BaseModel):

    """Schema of course run."""

    id: str
    course_id: str
    name: str

    @staticmethod
    def from_domain(course_run: CourseRunEntity) -> "CourseRunDTO":
        return CourseRunDTO(
            id=course_run.id.value,
            course_id=course_run.course_id.value,
            name=course_run.name.value,
        )
