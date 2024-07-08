import datetime
import uuid

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.auth.entities import UserEntity
from src.domain.auth.value_objects import PartOfName, Email, UserRole
from src.infrastructure.sqlalchemy.session import Base


class User(Base):

    """SQLAlchemy model of User."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )

    def to_domain(self):
        return UserEntity(
            id=str(self.id),
            firstname=PartOfName(self.firstname),
            lastname=PartOfName(self.lastname),
            role=UserRole(self.role),
            email=Email(self.email),
            hashed_password=self.hashed_password,
        )

    @staticmethod
    def from_domain(user: UserEntity):
        return User(
            id=str(user.id),
            firstname=user.firstname.value,
            lastname=user.lastname.value,
            role=user.role.value,
            email=user.email.value,
            hashed_password=user.hashed_password,
        )
