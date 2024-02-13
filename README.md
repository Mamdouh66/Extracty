# ScraperGPT

A fun, useful project I made a while ago when making a bigger project and thought of sharing it.

The main idea of the project is to make scraping websites much faster with the use of LLMs to extract the needed information in `JSON` format with just defining a `pydantic` schema. So, you don't need to manually define a parsing way for each website and a lot of boring stuff...

## Project Structure

The main file is `src/`

`main.py`: This is the main entry point for the application. It orchestrates the scraping process, it has a simple script to check the logic.  
`web_scraper.py`: This file contains the functions for scraping web pages with using two choices `requests` and `playwright`.
`gpt_scraper.py`: This file contains helper functions for `web_scraper.py` for processing the scraped content using GPT.
`config.py`: This file contains configuration settings for the project.
`schemas.py`: This file defines the schemas used to extract information from the scraped content

## How to Run

first install the requirements.

```bash
pip install requirements.txt
```

then to run the main file from the src, run it relatively (ik its not best practice).

```bash
python -m src.main
```

## How to Run Tests

to run all the tests do the following.

```bash
pytest tests/
```

## Note

Before running the project, make sure to set your OpenAI API key in the .env file

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the original repository.

I appreciate your contributions to build this fun project!
