import re

EMAIL_REGULAR_EXPRESSION = r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}"
EMAIL_PATTERN = re.compile(EMAIL_REGULAR_EXPRESSION)
ADMIN_ROLE = "admin"
TALENT_ROLE = "talent"
USER_ROLES = [ADMIN_ROLE, TALENT_ROLE]
PASSWORD_MIN_LENGTH = 8
TIME_TO_LIVE_AUTH_SESSION = 60 * 60 * 24
