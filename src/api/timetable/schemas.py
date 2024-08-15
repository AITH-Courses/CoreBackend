import datetime

from pydantic import BaseModel

from src.domain.timetable.entities import TimetableEntity


class LessonDTO(BaseModel):
    start_time: datetime.time
    end_time: datetime.time
    date: datetime.date


class TimetableDTO(BaseModel):
    lessons: list[LessonDTO]

    @staticmethod
    def from_domain(timetable: TimetableEntity) -> "TimetableDTO":
        current_lessons = timetable.lessons
        return TimetableDTO(
            lessons=[
                LessonDTO(
                    start_time=lesson.start_time.time(),
                    end_time=lesson.start_time.time(),
                    date=lesson.start_time.date()
                ) for lesson in current_lessons]
        )
