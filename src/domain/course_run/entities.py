from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.base_value_objects import UUID
    from src.domain.courses.value_objects import CourseRun


@dataclass
class CourseRunEntity:

    """Entity of timetable."""

    id: UUID
    course_id: UUID
    name: CourseRun

    def is_actual_by_date(self, current_date: datetime.date) -> bool:
        month, year = current_date.month, current_date.year
        run_season, run_year = self.name.season, self.name.year
        if run_season == "Осень":
            # С предзаписи и до конца осеннего семестра
            return year == run_year and month in (8, 9, 10, 11, 12) or year == run_year + 1 and month == 1
        # С предзаписи и до конца весеннего семестра
        return year == run_year and month in (1, 2, 3, 4, 5, 6, 7)
