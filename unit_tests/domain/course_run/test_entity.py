import uuid

import pytest

from src.domain.base_value_objects import UUID
from src.domain.course_run.entities import CourseRunEntity
from src.domain.courses.exceptions import IncorrectCourseRunNameError
from src.domain.courses.value_objects import CourseRun


def test_correct_course_run():
    course_run = CourseRunEntity(
        id=UUID(str(uuid.uuid4())),
        name=CourseRun("Весна 2025"),
        course_id=UUID(str(uuid.uuid4()))
    )
    assert course_run.name.value == "Весна 2025"


@pytest.mark.parametrize("name", [
    "Зима 2024",
    "Весна",
    "2024",
    "2024 Весна"
])
def test_incorrect_course_run(name):
    with pytest.raises(IncorrectCourseRunNameError):
        CourseRunEntity(
            id=UUID(str(uuid.uuid4())),
            name=CourseRun(name),
            course_id=UUID(str(uuid.uuid4()))
        )
