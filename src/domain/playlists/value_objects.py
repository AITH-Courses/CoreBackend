from dataclasses import dataclass

from src.domain.courses.exceptions import ValueDoesntExistError
from src.domain.playlists.constants import VIDEO_RESOURCE_TYPES


@dataclass(init=False, eq=True, frozen=True)
class VideoResourceType:

    """Video resource type as a value object: vk, youtube."""

    value: str

    def __init__(self, value: str) -> None:
        """Initialize object.

        :param value:
        """
        if value not in VIDEO_RESOURCE_TYPES:
            raise ValueDoesntExistError(property_name="тип видеоресурса")
        object.__setattr__(self, "value", value)
