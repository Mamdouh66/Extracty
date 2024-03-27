import instructor

from openai import OpenAI
from pydantic import BaseModel, Field, create_model, validator
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from structify.config import settings
from structify import WebScraper

from typing import Type, Dict, Union, TypeVar

T = TypeVar("T", bound=BaseModel)

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
    def __init__(self, query: str, url: str, fields: list[str] | None = None):
        self.query = query
        self.url = url
        self.fields = fields

    async def _get_content(self) -> str:
            """
            Retrieves the content of a web page using a WebScraper object.

            Returns:
                str: The content of the web page.

            Raises:
                TimeoutError: If the scraping process times out or the page takes too long to load.
                Exception: If any other exception occurs during the scraping process.
            """
            scraper = WebScraper(self.url)
            try:
                content = await scraper.ascraping_with_playwright()
                return content
            except PlaywrightTimeoutError as pte:
                raise TimeoutError(
                    "The scraping process timed out. Or the page took too long to load. Please try again later."
                )
            except Exception as e:
                raise e

    def _create_pydantic_model(self, fields: Dict[str, Type]) -> Type[T]:
        """
        Create a Pydantic model dynamically based on fields provided

        Args:
            fields (Dict[str, Type]): A dictionary containing the field names and their corresponding types.

        Returns:
            BaseModel: The dynamically created Pydantic model.

        """
        field_definitions = {
            field_name: (field_type, Field(...))
            for field_name, field_type in fields.items()
        }
        dynamic_model = create_model("CustomExtractor", **field_definitions)
        return dynamic_model
