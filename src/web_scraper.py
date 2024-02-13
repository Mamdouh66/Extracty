import logging
import requests

from bs4 import BeautifulSoup
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
from pydantic import BaseModel
from typing import Type, Union

from .config import settings
from .gpt_scraper import extract

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def clean_html_content(
    html_content: str, tags: list[str], unwanted_tags: list[str] = ["script", "style"]
) -> str:
    from bs4 import BeautifulSoup

    # Remove unwanted tags
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    # Extract text from wanted tags
    text_parts = []
    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            if tag == "a":
                href = element.get("href")
                text_parts.append(
                    f"{element.get_text()} ({href})" if href else element.get_text()
                )
            else:
                text_parts.append(element.get_text())

    # Remove unnecessary lines
    content = " ".join(text_parts)
    lines = content.split("\n")
    stripped_lines = [line.strip() for line in lines]
    non_empty_lines = [line for line in stripped_lines if line]
    seen = set()
    deduped_lines = [
        line for line in non_empty_lines if not (line in seen or seen.add(line))
    ]
    cleaned_content = " ".join(deduped_lines)

    return cleaned_content


async def ascraping_with_playwright(
    url: str,
    schema: Union[Type[BaseModel], BaseModel],
    tags: list[str] = ["h1", "h2", "h3", "span", "p", "a"],
):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            page.set_default_navigation_timeout(60000)
            await page.goto(url)
            page_source = await page.content()
            cleaned_content = clean_html_content(page_source, tags)
            return extract(cleaned_content[: settings.GPT_LIMIT], schema)
    except PlaywrightTimeoutError as e:
        logging.error(f"Playwright Timeout Error: {e}")
        raise
    except Exception as e:
        logging.error(f"Scraping Error: {e}")
        raise


def scraping_with_requests(
    url: str,
    schema: Union[Type[BaseModel], BaseModel],
    tags: list[str] = ["h1", "h2", "h3", "span", "p", "a"],
    gpt=True,
):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        cleaned_content = clean_html_content(response.text, tags)
        if gpt:
            return extract(cleaned_content[: settings.GPT_LIMIT], schema)
    except requests.RequestException as e:
        logging.error(f"Requests Error: {e}")
        raise
    return cleaned_content
