# Extracty: Dynamic Data Extraction

Extract structured data from any unstructered web page

extracty is a library designed to streamline and simplify the process of extracting structured data from websites. Utilizing the robust functionality of Pydantic and Instructor, extracty enables users to define dynamic data extraction schemas and interact with a simple function call.

## How to Run

first install the library.

```bash
pip install extracty
```

How to use the library

```python
from extracty import LLMExtractor

extractor = LLMExtractor(
    url="url-you-want-to-scrape",
    query="your-query",
    api_key="your-openai-api-key",
)

data = extractor.extract()

print(data.model_dump_json())
```

more advance extraction

here you can specify the `fields` you want the model to look for.  
Also, you can specify the types you want for each model for easier data handling.

```python
from extracty import LLMExtractor

fields = {
    "feild_1": str,
    "feild_2": int,
    "field_3": bool,
}

extractor = LLMExtractor(
    url="url-you-want-to-scrape",
    query="your-query",
    api_key="your-openai-api-key",
    fields=fields,
    gpt_model="the-model-you-want-to-use (defaults to gpt-4)",
)

data = extractor.extract()

print(data.model_dump_json())
```

## Example-usage

Here is an example usage where we want to get the top 5 trending github repo's

```python
from extracty import LLMExtractor

fields = {
    "rank": int,
    "repo_name": str,
    "small_description": str,
}

extractor = LLMExtractor(
    url="https://www.github.com/trending",
    query="What are the top 5 trending repositories on GitHub?",
    api_key="your-openai-api-key",
    fields=fields,
    gpt_model="the-model-you-want-to-use (defaults to gpt-4)",
)

data = extractor.extract()

print(data.model_dump_json())
```

and the corresponding output

```json
{
  "name": "Top 5 Trending Repositories on GitHub",
  "data": [
    {
      "rank": 1,
      "repo_name": "stitionai / devika",
      "small_description": "Devika is an Agentic AI Software Engineer that can understand high-level human instructions, break them down into steps, research relevant information, and write code to achieve the given objective. Devika aims to be a competitive open-source alternative to Devin by Cognition AI."
    },
    {
      "rank": 2,
      "repo_name": "OpenDevin / OpenDevin",
      "small_description": "OpenDevin: Code Less, Make More 利用大模型，一键生成短视频"
    },
    {
      "rank": 3,
      "repo_name": "harry0703 / MoneyPrinterTurbo",
      "small_description": "Decentralized Autonomous Regulated Company (DARC), a company virtual machine that runs on any EVM-compatible blockchain, with on-chain law system, multi-level tokens and dividends mechanism."
    },
    {
      "rank": 4,
      "repo_name": "Project-DARC / DARC",
      "small_description": "A natural language interface for computers"
    },
    {
      "rank": 5,
      "repo_name": "OpenInterpreter / open-interpreter",
      "small_description": "A one stop repository for generative AI research updates, interview resources, notebooks and much more!"
    }
  ]
}
```

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the original repository.

I appreciate your contributions to build this fun project!

## TODOs

- [ ] Enhance the scraping and make it more robust.
  - [ ] Utilize async Playwright to be efficient for installation.
  - [ ] Enhance cleaning HTML content and make it more efficient.
- [ ] Enhance Pydantic modeling.
  - [ ] Enhance dynamic model creation.
  - [ ] Enhance BaseExtractor.
- [ ] Optimize performance for large-scale data extraction.

## Acknowledgments

Utilizes OpenAI for advanced data extraction capabilities.
Leverages Pydantic and Instructor for dynamic and robust data modeling.
Employs langchain, playwright for efficient web interaction.
