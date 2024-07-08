import pytest

from src.domain.auth.exceptions import EmailNotValidError, RoleDoesntExistError, EmptyPartOfNameError
from src.domain.auth.value_objects import Email, USER_ROLES, UserRole, PartOfName
from src.domain.courses.exceptions import EmptyPropertyError, ValueDoesntExistError, IncorrectCourseRunNameError
from src.domain.courses.value_objects import CourseName, Author, Implementer, Format, CourseRun
from src.domain.courses.constants import IMPLEMENTERS, FORMATS, TERMS, ROLES, PERIODS


def test_correct_course_name():
    course_name_string = "Python"
    course_name = CourseName(course_name_string)
    assert course_name.value == course_name_string


def test_incorrect_course_name():
    with pytest.raises(EmptyPropertyError):
        CourseName("")


def test_correct_author():
    author_string = "Иванов И.И., ктн"
    author = Author(author_string)
    assert author.value == author_string


def test_incorrect_author():
    with pytest.raises(EmptyPropertyError):
        Author("")


def test_correct_implementer():
    implementer_string = IMPLEMENTERS[0]
    implementer = Implementer(implementer_string)
    assert implementer.value == implementer_string


def test_incorrect_implementer():
    with pytest.raises(ValueDoesntExistError):
        Implementer("Неизвестный реализатор")


def test_correct_format():
    format_string = FORMATS[0]
    format_ = Format(format_string)
    assert format_.value == format_string


def test_incorrect_format():
    with pytest.raises(ValueDoesntExistError):
        Format("Неизвестный формат")


def test_correct_run():
    run_string = "Весна 2023"
    run = CourseRun(run_string)
    assert run.value == run_string


@pytest.mark.parametrize("run_name", [
    "", "Весна", "Весна 1992", "Весна 2992", "Зима 2023", "2034",
])
def test_incorrect_run(run_name):
    with pytest.raises(IncorrectCourseRunNameError):
        CourseRun(run_name)
