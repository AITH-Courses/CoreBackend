import os
import hashlib

from src.domain.auth.constants import PASSWORD_MIN_LENGTH
from src.domain.auth.exceptions import PasswordTooShortError, WrongPasswordError


class PasswordService:
    @staticmethod
    def validate_password(password: str) -> None:
        if len(password) < PASSWORD_MIN_LENGTH:
            raise PasswordTooShortError

    @staticmethod
    def create_hashed_password(password: str) -> str:
        salt = os.urandom(32)
        encoded_password = password.encode("UTF-8")
        key = hashlib.pbkdf2_hmac('sha256', encoded_password, salt, 100000)
        return key.hex() + "." + salt.hex()

    @staticmethod
    def verify_password(try_password: str, hashed_password: str) -> None:
        encoded_try_password = try_password.encode("UTF-8")
        key, salt = hashed_password.split(".")
        try_key = hashlib.pbkdf2_hmac('sha256', encoded_try_password, bytes.fromhex(salt), 100000)
        real_key = bytes.fromhex(key)
        if try_key != real_key:
            raise WrongPasswordError
