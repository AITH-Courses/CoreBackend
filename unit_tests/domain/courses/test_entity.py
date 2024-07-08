import pytest

from src.domain.courses.entities import CourseEntity
from src.domain.courses.exceptions import CoursePublishError
from src.domain.courses.constants import IMPLEMENTERS, ROLES, FORMATS, PERIODS, TERMS
from src.domain.courses.value_objects import CourseName, Author, Implementer, Format, Terms, Role, CourseRun, Period


def test_correct_course():
    course = CourseEntity(
        id="fs4sdg4gs",
        name=CourseName("Java"),
    )
    assert course.id == "fs4sdg4gs"
    assert course.name == CourseName("Java")
    assert course.image_url is None
    assert len(course.roles) != []


def test_publish_empty_course():
    course = CourseEntity(
        id="fs4sdg4gs",
        name=CourseName("Java"),
    )
    with pytest.raises(CoursePublishError):
        course.publish()


def test_publish_already_published_course():
    course = CourseEntity(
        id="fs4sdg4gs",
        name=CourseName("Java"),
        is_draft=False
    )
    with pytest.raises(CoursePublishError):
        course.publish()


def test_publish_full_course():
    course = CourseEntity(
        id="fs4sdg4gs",
        name=CourseName("Java"),
        image_url="path-to-logo.jpg",
        author=Author("Иванов И. И."),
        implementer=Implementer(IMPLEMENTERS[0]),
        format=Format(FORMATS[0]),
        terms=Terms(TERMS[0]),
        roles=[Role(ROLES[0])],
        periods=[Period(PERIODS[0])],
        last_runs=[CourseRun("Весна 2023")],
    )
    course.publish()
    assert not course.is_draft


def test_hide_draft_course():
    course = CourseEntity(
        id="fs4sdg4gs",
        name=CourseName("Java"),
        image_url="path-to-logo.jpg",
        author=Author("Иванов И. И."),
        implementer=Implementer(IMPLEMENTERS[0]),
        format=Format(FORMATS[0]),
        terms=Terms(TERMS[0]),
        roles=[Role(ROLES[0])],
        periods=[Period(PERIODS[0])],
    )
    with pytest.raises(CoursePublishError):
        course.hide()


def test_hide_published_course():
    course = CourseEntity(
        id="fs4sdg4gs",
        name=CourseName("Java"),
        is_draft=False
    )
    course.hide()
    assert course.is_draft
