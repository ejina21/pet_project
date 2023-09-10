from typing import Literal
from pydantic import AnyUrl, field_validator, PostgresDsn, RedisDsn
from ipaddress import IPv4Address
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']
    LOG_LEVEL: str

    DB_SCHEME: str
    DB_HOST: IPv4Address | AnyUrl
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    TEST_DB_HOST: IPv4Address | AnyUrl
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str

    SECRET_KEY: str
    ALGORITHM: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    @field_validator('DB_PORT', 'REDIS_PORT', 'SMTP_PORT', 'TEST_DB_PORT')
    def validate_port(cls, v: int) -> int:
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @field_validator('DB_SCHEME')
    def validate_pg_scheme(cls, v: int) -> PostgresDsn:
        allowed_schemes = PostgresDsn.__metadata__[0].allowed_schemes
        if v not in allowed_schemes:
            raise ValueError('Invalid PostgresDsn scheme')
        return v

    @field_validator('REDIS_SCHEME')
    def validate_rds_scheme(cls, v: int) -> RedisDsn:
        allowed_schemes = RedisDsn.__metadata__[0].allowed_schemes
        if v not in allowed_schemes:
            raise ValueError('Invalid RedisDsn scheme')
        return v

    @property
    def database_url(self) -> str:
        return PostgresDsn.build(
            scheme=self.DB_SCHEME,
            username=self.DB_USER,
            password=self.DB_PASS,
            host=str(self.DB_HOST),
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    @property
    def test_database_url(self) -> str:
        return PostgresDsn.build(
            scheme=self.DB_SCHEME,
            username=self.TEST_DB_USER,
            password=self.TEST_DB_PASS,
            host=str(self.TEST_DB_HOST),
            port=self.TEST_DB_PORT,
            path=self.TEST_DB_NAME,
        )

    REDIS_SCHEME: str
    REDIS_HOST: IPv4Address | AnyUrl
    REDIS_PORT: int

    @property
    def redis_url(self) -> str:
        return RedisDsn.build(
            scheme=self.REDIS_SCHEME,
            host=str(self.REDIS_HOST),
            port=str(self.REDIS_PORT)
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
