from structify import LLMExtractor

url = "https://github.com/trending"

extractor = LLMExtractor(
    query="what are the top 5 trending repositories and their details?",
    url=url,
    fields={"rank": int, "name": str, "description": str},
)

data = extractor.extract()

print(data.model_dump_json())

with open("trending_repositories.json", "w") as f:
    f.write(data.model_dump_json())
