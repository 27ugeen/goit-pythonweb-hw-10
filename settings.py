from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr 
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_FROM_NAME: str = "Your App"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()