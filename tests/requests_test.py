import pytest
import requests

from unittest.mock import Mock
from pydantic import BaseModel

from src import web_scraper


def test_web_scraping_success():
    result = web_scraper.scraping_with_requests(
        "https://www.scrapethissite.com/pages/simple/",
        schema=BaseModel,
        gpt= False
    )
    with open("content.txt", "r") as f:
        content = f.read()
    assert result == content


def test_web_scraping_http_error():
    requests.get = Mock(side_effect=requests.exceptions.HTTPError("HTTP Error"))
    result = web_scraper.scraping_with_requests(
        "https://httpbin.org/get", schema=BaseModel
    )
    assert result == "HTTP Error: HTTP Error"


def test_web_scraping_connection_error():
    requests.get = Mock(
        side_effect=requests.exceptions.ConnectionError("Connection Error")
    )
    result = web_scraper.scraping_with_requests(
        "https://httpbin.org/get",
        schema=BaseModel,
    )
    assert result == "Connection Error: Connection Error"


def test_web_scraping_timeout_error():
    requests.get = Mock(side_effect=requests.exceptions.Timeout("Timeout Error"))
    result = web_scraper.scraping_with_requests(
        "https://httpbin.org/get",
        schema=BaseModel,
    )
    assert result == "Timeout Error: Timeout Error"


def test_web_scraping_request_error():
    requests.get = Mock(
        side_effect=requests.exceptions.RequestException("Request Error")
    )
    result = web_scraper.scraping_with_requests(
        "https://httpbin.org/get",
        schema=BaseModel,
    )
    assert result == "Request Error: Request Error"
