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
from youtube_transcript_api import YouTubeTranscriptApi

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

def extract_text_from_youtube(url: str) -> Optional[str]:
    """Fetch and extract the transcript from a YouTube URL robustly."""
    try:
        # Robust 11-char regex for YouTube Video IDs
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
        if not match: 
            return "Error: Could not extract an 11-character YouTube video ID from the URL."
        video_id = match.group(1)
        
        try:
            # 1. Fetch transcript metadata
            yt_api = YouTubeTranscriptApi()
            transcript_list = yt_api.list(video_id)
            
            # 2. Try manual english, then auto english, then translate whatever exists
            try:
                transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB']).fetch()
            except Exception:
                try:
                    transcript = transcript_list.find_generated_transcript(['en', 'en-US', 'en-GB']).fetch()
                except Exception:
                    # Grab whatever the first transcript language is, and translate it to English
                    for t in transcript_list:
                        transcript = t.translate('en').fetch()
                        break
        except Exception as e:
            # Final fallback directly to the raw getter
            yt_api = YouTubeTranscriptApi()
            transcript = yt_api.fetch(video_id)
            
        text = " ".join([getattr(t, "text", "") if hasattr(t, "text") else t.get("text", "") for t in transcript])
        return text.replace("  ", " ").strip()
    except Exception as e:
        return f"Error: {str(e)}"

