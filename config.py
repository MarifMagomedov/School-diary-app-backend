from environs import Env
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str


def load_database_config() -> DatabaseConfig:
    env = Env()
    env.read_env()
    return DatabaseConfig(
        db_name=env.str("DB_NAME"),
        db_user=env.str("DB_USER"),
        db_pass=env.str("DB_PASS"),
        db_host=env.str("DB_HOST"),
        db_port=env.str("DB_PORT")
    )
