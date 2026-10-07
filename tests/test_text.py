import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from fakestyle.text import strip_text, strip_title, truncate_words  # noqa: E402


def test_reuters_dateline_removed():
    assert strip_text("WASHINGTON (Reuters) - The Senate voted on Tuesday.") == "The Senate voted on Tuesday."
    assert strip_text("RIO DE JANEIRO/SAO PAULO (Reuters) - Billionaire released.") == "Billionaire released."


def test_plain_dash_kept_without_agency_tag():
    text = "Obama - the former president - spoke."
    assert strip_text(text) == text


def test_title_publisher_and_media_tags():
    assert strip_title("Senators Propose Plan - The New York Times") == "Senators Propose Plan"
    assert strip_title("No Change For ESPN - Breitbart") == "No Change For ESPN"
    assert strip_title("JOE BIDEN'S SHOCKING ANNOUNCEMENT [Video]") == "JOE BIDEN'S SHOCKING ANNOUNCEMENT"
    assert strip_title("Spicer Baffles Reporters (VIDEO)") == "Spicer Baffles Reporters"


def test_credits_urls_and_embeds_removed():
    text = ("He said it was over. Featured image via Getty Images.\n"
            "See https://t.co/abc123 now. CNN (@CNN) December 6, 2016\n"
            "— Jane Doe (@janedoe) November 5, 2016\nRead more: Daily Wire")
    out = strip_text(text)
    for gone in ("Featured image", "Getty", "https://", "@janedoe", "Read more"):
        assert gone not in out, gone
    assert out.startswith("He said it was over.")


def test_truncate_cuts_at_sentence_end():
    text = " ".join(["word"] * 250) + ". " + " ".join(["more"] * 100) + "."
    out = truncate_words(text, max_words=300, min_words=200)
    assert out.endswith("word.")
    assert len(out.split()) == 250


def test_truncate_short_text_unchanged():
    assert truncate_words("A short text.", 300) == "A short text."


def test_ordinary_sentences_survive():
    text = "Via the new program, a photo by the agency showed the Getty museum. Read the report."
    assert strip_text(text) == text
