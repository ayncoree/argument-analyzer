"""
parser.py — Next-Gen Argument Parser with Multi-Source Support

Features:
- Abbreviation-aware sentence splitting
- Web scraper (URL → Text)
- PDF reader (File → Text)
- Text cleanup and normalization
"""

import re
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
import PyPDF2

# Common abbreviations
_ABBREVS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "vs", "etc", "e.g", "i.e",
    "a.m", "p.m", "u.s", "u.k", "jan", "feb", "mar", "apr", "jun", "jul",
    "aug", "sep", "oct", "nov", "dec",
}

_SENT_BOUNDARY = re.compile(r'(?<=[.!?])\s+(?=[A-Z"])')

def _protect_abbreviations(text: str) -> str:
    placeholder = "⟨DOT⟩"
    def _repl(m: re.Match) -> str:
        token = m.group(0)
        base = token.rstrip(".").lower()
        if base in _ABBREVS:
            return token.replace(".", placeholder)
        return token
    return re.sub(r'\b[A-Za-z]+\.', _repl, text)

def _restore_abbreviations(text: str) -> str:
    return text.replace("⟨DOT⟩", ".")

def split_sentences(text: str) -> List[str]:
    if not text or not text.strip():
        return []
    # Normalise unicode
    text = (
        text.replace("\u2018", "'").replace("\u2019", "'")
            .replace("\u201c", '"').replace("\u201d", '"')
            .replace("\u2014", " — ").replace("\u2013", " – ")
            .replace("\u2026", "...")
    )
    # Collapse newlines
    text = re.sub(r'\n+', ' ', text).strip()
    protected = _protect_abbreviations(text)
    raw_sentences = _SENT_BOUNDARY.split(protected)
    sentences = []
    for s in raw_sentences:
        s = _restore_abbreviations(s).strip()
        s = s.strip('"').strip()
        if len(s) >= 4:
            sentences.append(s)
    return sentences

# ─── New Source Handlers ───────────────────────────────────────────────────

def extract_text_from_url(url: str) -> Optional[str]:
    """Fetch and extract the main article text from a URL."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200: return None
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        # Typical content containers
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return "\n".join(chunk for chunk in chunks if chunk)
    except Exception:
        return None

def extract_text_from_pdf(file_obj) -> Optional[str]:
    """Read and extract text from a PDF file object."""
    try:
        reader = PyPDF2.PdfReader(file_obj)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception:
        return None
