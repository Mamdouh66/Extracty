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
                        "text": "Some Quotes",
                        "author": "Some Author",
                        "tags": '["tag1", "tag2"] if any',
                    },
                ]
            }
        }
