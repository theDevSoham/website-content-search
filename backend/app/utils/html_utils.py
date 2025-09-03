# app/utils/html_utils.py
import re
import requests
from bs4 import BeautifulSoup

def fetch_html(url: str) -> str:
    """Fetch and clean HTML content from a URL."""
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove scripts/styles
    for tag in soup(["script", "style"]):
        tag.extract()

    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text
