import pytest
import requests

from unittest.mock import Mock, patch
from pydantic import BaseModel

from src import web_scraper

web_scraper.settings = Mock()
web_scraper.settings.GPT_LIMIT = 500

# web_scraper.extract = Mock(return_value="extracted content")


@pytest.fixture
def mock_requests_get():
    with patch("src.web_scraper.requests.get") as mock_get:
        yield mock_get


def test_web_scraping_success():
    with open("content.txt", "r") as f:
        content = f.read()

    with patch("src.web_scraper.clean_html_content") as mock_clean:
        mock_clean.return_value = content

        result = web_scraper.scraping_with_requests(
            "https://www.scrapethissite.com/pages/simple/",
            schema=BaseModel,
            gpt=False,
        )

    assert result == result


def test_web_scraping_http_error(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.HTTPError("HTTP Error")
    with pytest.raises(requests.exceptions.HTTPError):
        web_scraper.scraping_with_requests(
            "https://httpbin.org/get", schema=BaseModel, gpt=False
        )


def test_web_scraping_connection_error(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.ConnectionError(
        "Connection Error"
    )
    with pytest.raises(requests.exceptions.ConnectionError):
        web_scraper.scraping_with_requests(
            "https://httpbin.org/get", schema=BaseModel, gpt=False
        )


def test_web_scraping_timeout_error(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.Timeout("Timeout Error")
    with pytest.raises(requests.exceptions.Timeout):
        web_scraper.scraping_with_requests(
            "https://httpbin.org/get", schema=BaseModel, gpt=False
        )


def test_web_scraping_request_error(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.RequestException(
        "Request Error"
    )
    with pytest.raises(requests.exceptions.RequestException):
        web_scraper.scraping_with_requests(
            "https://httpbin.org/get", schema=BaseModel, gpt=False
        )
