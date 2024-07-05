import pytest

from src.domain.auth.exceptions import EmailNotValidError, RoleDoesntExistError, EmptyPartOfNameError
from src.domain.auth.value_objects import Email, USER_ROLES, UserRole, PartOfName


def test_correct_email():
    email_string = "john@gmail.com"
    email = Email(email_string)
    assert email.value == email_string


@pytest.mark.parametrize("email_string", [
    "gmail.com", "johny", "joe@", "@joe", "@@@"
])
def test_incorrect_email(email_string):
    with pytest.raises(EmailNotValidError):
        Email(email_string)


def test_correct_role():
    role_string = USER_ROLES[0]
    role = UserRole(role_string)
    assert role.value == role_string


def test_incorrect_role():
    role_string = "another"
    with pytest.raises(RoleDoesntExistError):
        UserRole(role_string)


def test_correct_part_of_name():
    part_of_name_string = "Johny"
    role = PartOfName(part_of_name_string)
    assert role.value == part_of_name_string


def test_incorrect_part_of_name():
    part_of_name_string = ""
    with pytest.raises(EmptyPartOfNameError):
        PartOfName(part_of_name_string)