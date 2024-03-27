import instructor

from openai import OpenAI
from pydantic import BaseModel, Field, create_model, validator

from structify.config import settings

client = instructor.patch(OpenAI(api_key=settings.OPENAI_API_KEY))


class BaseExtractor(BaseModel):
    """
    Base schema for extractors.

    Pydantic schemas will be used with the help of instructor to make structured prompts and it will make the extraction process easier.

    Attributes:
        name (str): The name of the extracted thing.
        data (list[dict[str, str]]): The important data to be extracted.
    """

    name: str = Field(
        ...,
        description="The name of extracted thing",
        examples=["latest_stock_details", "trending_news"],
    )
    data: list[dict[str, str]] = Field(
        description="The important data to be extracted",
        examples=[{"Harry Potter": "Gryiffindor"}, {"Draco Malfoy": "Slytherin"}],
    )

    @validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("The name must be a non-empty string.")
        return v

    @validator("data", each_item=True)
    def validate_data(cls, v):
        if not isinstance(v, dict):
            raise TypeError("Each item in data must be a dictionary.")
        if not all(
            isinstance(key, str) and isinstance(value, str) for key, value in v.items()
        ):
            raise ValueError(
                "Each dictionary in data must have string keys and values."
            )
        return v


class LLMExtractor:
    def __init__(self): ...
