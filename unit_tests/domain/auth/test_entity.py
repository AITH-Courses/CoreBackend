import uuid

from src.domain.auth.entities import UserEntity
from src.domain.auth.value_objects import PartOfName, UserRole, Email
from src.domain.base_value_objects import UUID


def test_correct_user():
    user = UserEntity(
        id=UUID(str(uuid.uuid4())),
        firstname=PartOfName("Nick"),
        lastname=PartOfName("Cargo"),
        role=UserRole("admin"),
        email=Email("nick@cargo.com"),
        hashed_password="32rserfs4t4ts4t4"
    )
    assert user.role == UserRole("admin")
    assert user.firstname == PartOfName("Nick")
    assert user.lastname == PartOfName("Cargo")
    assert user.email == Email("nick@cargo.com")
    assert user.hashed_password == "32rserfs4t4ts4t4"
