import asyncio
from src import web_scraper
from schemas import WebsiteSchema


async def main() -> None:
    # URL = "https://www.therundown.ai/p/lucid-dreaming-with-ai"

    # content = web_scraper.scraping_with_requests(URL)

    # with open("content.txt", "w") as f:
    #     f.write(content)

    res = web_scraper.scraping_with_requests(
        "https://www.scrapethissite.com/pages/simple/"
    )

    with open("content.txt", "w") as f:
        f.write(res)


if __name__ == "__main__":
    asyncio.run(main())
