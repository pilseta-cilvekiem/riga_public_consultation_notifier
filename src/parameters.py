from os import environ, getenv
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs

from .enums.public_consultation_type import PublicConsultationType


def _get_enabled_public_consultation_types(
    public_consultation_types_string: str,
) -> list[PublicConsultationType]:
    public_consultation_type_strings = [
        public_consultation_type_string.strip()
        for public_consultation_type_string in public_consultation_types_string.split(
            ","
        )
    ]
    public_consultation_types = [
        PublicConsultationType(public_consultation_type_string)
        for public_consultation_type_string in public_consultation_type_strings
        if public_consultation_type_string
    ] or list(PublicConsultationType)
    return public_consultation_types


def _get_required_environment_variable(environment_variable_name: str) -> str:
    try:
        return environ[environment_variable_name]
    except KeyError as e:
        raise KeyError(
            f"Environment variable {environment_variable_name} is not set"
        ) from e


def _get_required_secret_value(secret_name: str) -> str:
    try:
        return _get_secret_value(secret_name)
    except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
        raise KeyError(f"Secret {secret_name} is not set") from e


def _get_optional_secret_value(secret_name: str) -> Optional[str]:
    try:
        return _get_secret_value(secret_name)
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        return None


def _get_secret_value(secret_name: str) -> str:
    secret_value = Path(f"{SECRET_DIR}/{secret_name}").read_text().strip()
    return secret_value


DATA_DIRECTORY = "data"
DATABASE_DRIVER = getenv("DATABASE_DRIVER")
DATABASE_HOST = getenv("DATABASE_HOST")
sqlalchemy_port_string = getenv("DATABASE_PORT")
DATABASE_NAME = getenv("DATABASE_NAME")
DATABASE_PORT = int(sqlalchemy_port_string) if sqlalchemy_port_string else None
DATABASE_QUERY_STRING_PARAMETERS = parse_qs(getenv("DATABASE_QUERY_STRING_PARAMETERS"))
DATABASE_USERNAME = getenv("DATABASE_USERNAME")
days_to_store_inactive_public_consultations = getenv(
    "DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS", 365
)
DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS = (
    int(days_to_store_inactive_public_consultations)
    if days_to_store_inactive_public_consultations
    else None
)
DEFAULT_DATABASE_URL = f"sqlite:///{DATA_DIRECTORY}/sqlite.db"
ENABLED_PUBLIC_CONSULTATION_TYPES = _get_enabled_public_consultation_types(
    getenv("ENABLED_PUBLIC_CONSULTATION_TYPES", "")
)
ROOT_URL = "https://www.riga.lv"
SECRET_DIR = getenv("SECRET_DIR", "secrets")
SLACK_CHANNEL_ID = _get_required_environment_variable("SLACK_CHANNEL_ID")
TIME_ZONE = getenv("TIME_ZONE", "Europe/Riga")


def get_slack_bot_user_oauth_token() -> str:
    return _get_required_secret_value("slack-bot-user-oauth-token")


def get_database_password() -> Optional[str]:
    return _get_optional_secret_value("database-password")
