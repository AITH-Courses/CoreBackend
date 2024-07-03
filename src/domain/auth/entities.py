from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from src.domain.auth.value_objects import Email, PartOfName, UserRole


@dataclass
class UserEntity:

    """Entity of user."""

    id: UUID | None
    firstname: PartOfName
    lastname: PartOfName
    role: UserRole
    email: Email
    hashed_password: str
