import logging
import requests

from bs4 import BeautifulSoup
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Playwright,
)
from pydantic import BaseModel

from .config import settings
from typing import Type, Union
from .gpt_scraper import extract

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def remove_unwanted_tags(
    html_content: str, unwanted_tags: list[str] = ["script", "style"]
) -> str:
    soup = BeautifulSoup(html_content, "html.parser")

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)


def extract_tags(html_content: str, tags: list[str]) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    text_parts = []

    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            if tag == "a":
                href = element.get("href")
                if href:
                    text_parts.append(f"{element.get_text()} ({href})")
                else:
                    text_parts.append(element.get_text())
            else:
                text_parts.append(element.get_text())

    return " ".join(text_parts)


def remove_unnecessary_lines(content: str) -> str:
    lines = content.split("\n")
    stripped_lines = [line.strip() for line in lines]
    non_empty_lines = [line for line in stripped_lines if line]
    seen = set()
    deduped_lines = [
        line for line in non_empty_lines if not (line in seen or seen.add(line))
    ]
    cleaned_content = "".join(deduped_lines)

    return cleaned_content


def clean_content(
    content: str, tags: list[str] = ["h1", "h2", "h3", "span", "p"]
) -> str:
    content_without_unwanted_tags = remove_unwanted_tags(content)
    content_after_extracting_tags = extract_tags(content_without_unwanted_tags, tags)
    results = remove_unnecessary_lines(content_after_extracting_tags)
    return results


async def run(
    playwright: Playwright, url: str, tags: list[str] = ["h1", "h2", "h3", "span", "p"]
) -> str:
    """
    Runs the web scraping process using Playwright.

    Args:
        playwright (Playwright): The Playwright instance.
        url (str): The URL of the webpage to scrape.
        tags (list[str], optional): The HTML tags to extract from the webpage. Defaults to ["h1", "h2", "h3", "span"].

    Returns:
        str: The scraped content.

    Raises:
        PlaywrightTimeoutError: If a timeout occurs during the scraping process.
        Exception: If any other error occurs during the scraping process.
    """
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    page.set_default_navigation_timeout(60000)
    try:
        await page.goto(url)

        page_source = await page.content()

        results = clean_content(content=page_source)

        logging.info("Content scraped...")

    except PlaywrightTimeoutError as pwte:
        results = f"TimeOut Error: {pwte}"
        logging.error(results)
    except Exception as e:
        results = f"Error: {e}"
        logging.error(results)

    return results


async def scrape(
    url: str,
    schema_pydantic: Union[Type[BaseModel], BaseModel],
    tags: list[str] = ["h1", "h2", "h3", "span", "p"],
):
    """
    Scrapes the specified URL using Playwright and extracts content using LLM.

    Args:
        url (str): The URL to scrape.
        tags (list[str], optional): The HTML tags to include in the scraping process. Defaults to ["h1", "h2", "h3", "span"].
        **kwargs: Additional keyword arguments to be passed to the ai_scraper.extract function.

    Returns:
        str: The extracted content.

    """
    async with async_playwright() as playwright:
        scraped_content = await run(playwright, url, tags)

    scraped_content_limit = scraped_content[: settings.GPT_LIMIT]

    logging.info("Extracting with LLM...")
    extracted_content = extract(
        content=scraped_content_limit, schema_pydantic=schema_pydantic
    )

    return extracted_content


def scraping_with_requests(url: str, tags: list[str] = ["h1", "h2", "h3", "span", "p"]):
    """
    Scrapes the specified URL using requests and extracts content using LLM.

    Args:
        url (str): The URL to scrape.
        tags (list[str], optional): The HTML tags to include in the scraping process. Defaults to ["h1", "h2", "h3", "span"].
        **kwargs: Additional keyword arguments to be passed to the ai_scraper.extract function.

    Returns:
        str: The extracted content.

    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        page = requests.get(url, headers=headers)
        page.raise_for_status()
        page_source = page.text

        results = clean_content(content=page_source)

        logging.info("Content scraped...")

    except requests.exceptions.HTTPError as e:
        results = f"HTTP Error: {e}"
        logging.error(results)
    except requests.exceptions.ConnectionError as e:
        results = f"Connection Error: {e}"
        logging.error(results)
    except requests.exceptions.Timeout as e:
        results = f"Timeout Error: {e}"
        logging.error(results)
    except requests.exceptions.RequestException as e:
        results = f"Request Error: {e}"
        logging.error(results)

    return results
