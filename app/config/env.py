from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: str
    DB_NAME: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    SCOPE: str
    PROJECT_ID: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"


settings = Settings()
