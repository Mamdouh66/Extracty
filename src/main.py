import asyncio
from .web_scraper import scraping_with_requests, ascraping_with_playwright
from .schemas import QuotesPage


async def main() -> None:
    content_with_requests = scraping_with_requests(
        url="http://quotes.toscrape.com/",
        schema=QuotesPage,
        gpt=True,
    )

    content_with_playwright = await ascraping_with_playwright(
        url="http://quotes.toscrape.com/",
        schema=QuotesPage,
    )

    with open("content_with_requests.json", "w") as f:
        f.write(content_with_requests)

    with open("content_with_playwright.json", "w") as f:
        f.write(content_with_playwright)


if __name__ == "__main__":
    asyncio.run(main())
