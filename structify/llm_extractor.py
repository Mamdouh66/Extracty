import asyncio
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
        description="The data to be extracted. It should be a list of dictionaries with key-value pairs.",
        examples=[{"Harry Potter": "Gryiffindor"}, {"Draco Malfoy": "Slytherin"}],
    )


class LLMExtractor:
    def __init__(self, query: str, url: str, fields: list[str] | None = None):
        self.query = query
        self.url = url
        self.fields = fields

    async def __get_content(self) -> str:
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

    def __create_pydantic_model(self, fields: Dict[str, Type]) -> Type[T]:
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
        dynamic_model = create_model(
            "CustomExtractor", **field_definitions, __base__=BaseModel
        )
        return dynamic_model

    def __generate_prompt(self, content: str) -> list[dict]:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful extractor that extract and structur data. You will be given a content to extract information from. The content is delimited by four backticks. Also, you will be given a query of what to extract delimited by four hashtags.",
            },
            {
                "role": "user",
                "content": f"please have the following Query: ####{self.query}#### and here is the following Content: ```{content}```",
            },
        ]
        return messages

    def __call_openai(self, prompt: list[dict], pydantic_schema: Type[T]) -> dict:
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=prompt,
            response_model=pydantic_schema,
            temperature=0.125,
        )
        return response

    def __async_run_content(self) -> str:
        """
        Runs the __get_content method asynchronously and returns the content.

        Returns:
            str: The content obtained from the __get_content method.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        content = loop.run_until_complete(self.__get_content())
        loop.close()
        return content

    def extract(self) -> str:
        """
        Extracts data from a web page using the OpenAI API.

        Returns:
            dict: The extracted data.

        Raises:
            TimeoutError: If the scraping process times out or the page takes too long to load.
            Exception: If any other exception occurs during the scraping process.
        """
        content = self.__async_run_content()

        pydantic_schema = (
            self.__create_pydantic_model(fields=self.fields)
            if self.fields
            else BaseExtractor
        )

        prompt = self.__generate_prompt(content)

        response = self.__call_openai(prompt=prompt, pydantic_schema=pydantic_schema)

        # TODO: implement more logic to handle response and create a structured output

        return response
