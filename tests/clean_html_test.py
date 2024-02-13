import pytest
from bs4 import BeautifulSoup
from src.web_scraper import clean_html_content


def test_clean_html_content_removes_unwanted_tags():
    html_content = "<html><body><script>console.log('Hello, world!');</script><p>Hello, world!</p></body></html>"
    cleaned_content = clean_html_content(html_content, ["p"])
    assert "<script>" not in cleaned_content
    assert "console.log('Hello, world!');" not in cleaned_content


def test_clean_html_content_extracts_text_from_specified_tags():
    html_content = (
        "<html><body><p>Hello, world!</p><div>Goodbye, world!</div></body></html>"
    )
    cleaned_content = clean_html_content(html_content, ["p"])
    assert "Hello, world!" in cleaned_content
    assert "Goodbye, world!" not in cleaned_content


def test_clean_html_content_formats_links_correctly():
    html_content = "<html><body><a href='https://example.com'>Example</a></body></html>"
    cleaned_content = clean_html_content(html_content, ["a"])
    assert "Example (https://example.com)" in cleaned_content


def test_clean_html_content_removes_extra_whitespace():
    html_content = "<html><body><p>   Hello, world!   </p><p>   Goodbye, world!   </p></body></html>"
    cleaned_content = clean_html_content(html_content, ["p"])
    assert "Hello, world!" in cleaned_content
    assert "   Hello, world!   " not in cleaned_content
    assert "Goodbye, world!" in cleaned_content
    assert "   Goodbye, world!   " not in cleaned_content


def test_clean_html_content_handles_empty_input():
    cleaned_content = clean_html_content("", ["p"])
    assert cleaned_content == ""


def test_clean_html_content_handles_invalid_input():
    with pytest.raises(TypeError):
        clean_html_content(None, ["p"])
