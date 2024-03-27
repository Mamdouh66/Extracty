from llm_extractor import LLMExtractor

url = "https://www.iau.edu.sa/"

extractor = LLMExtractor(
    query="what are the latest news and announcment about this university", url=url
)

data = extractor.extract()

print(data.model_dump_json())
