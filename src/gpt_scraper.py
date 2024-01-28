import time
import openai
import instructor

from .config import settings

from pydantic import BaseModel
from typing import Type, Union
from .schemas import WebsiteSchema

client = instructor.patch(openai.OpenAI(api_key=settings.OPENAI_API_KEY))

BASE_PROMPT: str = f"""
    You will be given HTML content of a web page it will be delimited by four hashtags.
    Please extract the following information according to the specified schema, and format it as a JSON:
    {
        str(WebsiteSchema.ConfigDict.json_schema_extra["example"])
    }
    """


def extract(content: str, schema_pydantic: Union[Type[BaseModel], BaseModel]):
    messages = [
        {
            "role": "system",
            "content": BASE_PROMPT,
        },
        {"role": "user", "content": f"This is the website content ####{content}####"},
    ]

    attempt = 0
    while attempt < settings.MAX_RETRIES:
        try:
            response: schema_pydantic = client.chat.completions.create(
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
