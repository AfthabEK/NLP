"""Text utilities shared by the notebooks: truncation and removal of source/publisher markers.

`strip_source_markers` removes cues that identify *where* an article came from rather than *what* it says
(agency tags, publisher suffixes, media tags, image credits, URLs, tweet embeds). It is used twice:
- notebook 03: the "stripped" condition, which separates the source-marker effect from the tone effect;
- notebook 04: the style-normalisation defense.
"""
import re

_SENTENCE_END = re.compile(r'[.!?]["\'”’)]?(?=\s|$)')

# --- title patterns -------------------------------------------------------------------------------
_TITLE_PUBLISHER = re.compile(r"\s+[-–—|]\s+(The New York Times|Breitbart|Reuters|The Onion)\s*$", re.I)
_TITLE_MEDIA_TAG = re.compile(r"\s*[\[(]\s*(?:video|videos|images?|photos?|watch|tweets?|audio)\s*[\])]", re.I)

# --- body patterns --------------------------------------------------------------------------------
_AGENCY_TAG = re.compile(r"\s*\((?:Reuters|AP|AFP|Bloomberg)\)\s*", re.I)
_LEADING_DASH = re.compile(r"^\s*([A-Z][A-Za-z .,/'-]{0,60}?)\s*[-–—]\s+")    # "WASHINGTON - " left after tag removal
_IMAGE_CREDIT = re.compile(
    r"\b(?:Featured image|Header image|Image via|Image credit|Photo credit|Photo via|Screenshot via)\b[^.\n]*\.?", re.I)
_GETTY = re.compile(r"\b(?:AFP/Getty Images|Getty Images)\b")
_READ_MORE = re.compile(r"\b(?:Read more|h/t)\s*:?[^\n]{0,120}?(?=\n|$)", re.I)
_VIA_LINE = re.compile(r"^\s*via\s*:?\s*[^\n]{0,60}$", re.I | re.M)
_TWEET_EMBED = re.compile(r"[—–-]\s*[^()\n]{0,60}\(@\w{1,30}\)\s+[A-Z][a-z]+ \d{1,2}, \d{4}")
_URL = re.compile(r"(?:https?://|www\.|pic\.twitter\.com/)\S+", re.I)
_HANDLE_VIA = re.compile(r"\bvia\s+@\w+", re.I)
_SPACES = re.compile(r"[ \t]{2,}")
_BLANKS = re.compile(r"\n{3,}")


def truncate_words(text: str, max_words: int = 300, min_words: int = 200) -> str:
    """First `max_words` words, cut back to the last sentence end if one falls after `min_words` words."""
    words = text.split()
    if len(words) <= max_words:
        return " ".join(words)
    cut = " ".join(words[:max_words])
    head_len = len(" ".join(words[:min_words]))
    ends = [m.end() for m in _SENTENCE_END.finditer(cut) if m.end() >= head_len]
    return cut[: ends[-1]] if ends else cut


def strip_title(title: str) -> str:
    title = _TITLE_PUBLISHER.sub("", title)
    title = _TITLE_MEDIA_TAG.sub("", title)
    return _SPACES.sub(" ", title).strip(" -–—|")


def strip_text(text: str) -> str:
    had_agency = bool(_AGENCY_TAG.search(text[:200]))
    text = _AGENCY_TAG.sub(" ", text)
    if had_agency:                                   # "WASHINGTON (Reuters) - Body" -> "Body"
        text = _LEADING_DASH.sub("", text, count=1)
    for pattern in (_TWEET_EMBED, _IMAGE_CREDIT, _GETTY, _READ_MORE, _VIA_LINE, _URL, _HANDLE_VIA):
        text = pattern.sub(" ", text)
    text = _SPACES.sub(" ", text)
    text = _BLANKS.sub("\n\n", text)
    return text.strip()


def strip_source_markers(title: str, text: str) -> tuple[str, str]:
    return strip_title(title), strip_text(text)
