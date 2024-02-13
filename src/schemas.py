from pydantic import BaseModel


class QuoteBase(BaseModel):
    text: str
    author: str
    tags: list[str] | None


class QuotesPage(BaseModel):
    quotes: list[QuoteBase]

    class ConfigDict:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "quotes": [
                    {
                        "text": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
                        "author": "Albert Einstein",
                        "tags": ["change", "deep-thoughts", "thinking", "world"],
                    },
                    {
                        "text": "It is our choices, Harry, that show what we truly are, far more than our abilities.",
                        "author": "J.K. Rowling",
                        "tags": ["abilities", "choices"],
                    },
                ]
            }
        }
