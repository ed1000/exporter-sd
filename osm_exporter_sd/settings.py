from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    lcm_password: str
    prometheus_password: str


settings = Settings()
