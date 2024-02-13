import time
import openai
import instructor

from .config import settings
from .schemas import QuotesPage

from pydantic import BaseModel
from typing import Type, Union

client = instructor.patch(openai.OpenAI(api_key=settings.OPENAI_API_KEY))

BASE_PROMPT: str = f"""
    You will be given HTML content of a web page it will be delimited by four hashtags.
    Please extract the following information according to the specified schema, and format it as a JSON:
    {
        str(QuotesPage.ConfigDict.json_schema_extra["example"])
    }
    """


def extract(
    content: str, schema: Union[Type[BaseModel], BaseModel], prompt: str = BASE_PROMPT
) -> str:
    messages = [
        {
            "role": "system",
            "content": prompt,
        },
        {"role": "user", "content": f"This is the website content ####{content}####"},
    ]

    attempt = 0
    while attempt < settings.MAX_RETRIES:
        try:
            response: schema = client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                temperature=0.125,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content

        except openai.APIConnectionError as e:
            print(f"Failed to connect to OpenAI API: {e}")
            attempt += 1
            time.sleep(2**attempt)

        except openai.RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            attempt += 1
            time.sleep(60)

        except openai.APIError as e:
            # Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            break

    return None
