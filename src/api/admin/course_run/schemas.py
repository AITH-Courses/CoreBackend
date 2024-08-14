from pydantic import BaseModel

from src.domain.course_run.entities import CourseRunEntity


class CreateCourseRunRequest(BaseModel):
    season: str
    year: int


class CreateCourseRunResponse(BaseModel):
    course_run_id: str


class CourseRunDTO(BaseModel):
    id: str
    course_id: str
    name: str

    @staticmethod
    def from_domain(course_run: CourseRunEntity) -> "CourseRunDTO":
        return CourseRunDTO(
            id=course_run.id.value,
            course_id=course_run.course_id.value,
            name=course_run.name.value
        )
