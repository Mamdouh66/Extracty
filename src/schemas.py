from pydantic import BaseModel


class WebsiteSchema(BaseModel):
    title: str
    content: str

    class ConfigDict:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "title": "Example Website Title",
                "content": "Detailed content of the website.",
            }
        }
