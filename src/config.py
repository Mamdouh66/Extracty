import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = "gpt-3.5-turbo-1106"
    # MODEL_NAME: str = "gpt-4-1106-preview"
    GPT_LIMIT: int = 16000
    MAX_RETRIES: int = 3


settings = Settings()
