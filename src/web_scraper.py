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
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in unwanted_tags:
        [element.decompose() for element in soup.find_all(tag)]
    text_parts = []
    for tag in tags:
        for element in soup.find_all(tag):
            text = (
                f"{element.get_text()} ({element.get('href')})"
                if tag == "a" and element.get("href")
                else element.get_text()
            )
            text_parts.append(text)

    cleaned_content = " ".join(
        {line.strip() for line in " ".join(text_parts).split("\n") if line.strip()}
    )
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
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        cleaned_content = clean_html_content(response.text, tags)
        if gpt:
            return extract(cleaned_content[: settings.GPT_LIMIT], schema)
    except requests.RequestException as e:
        logging.error(f"Requests Error: {e}")
        raise
