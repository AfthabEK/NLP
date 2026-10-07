# Style rewrites

LLM rewrites of 600 WELFake test articles (300 real, 300 fake), generated with Claude from the fixed prompt in
[`../prompts/rewrite_v1.md`](../prompts/rewrite_v1.md). The input is the article after source-marker stripping
and truncation to about 300 words (notebook 03a). Notebook 03b downloads these files from GitHub.

One file per input chunk, `chunk_XX.jsonl`, one JSON object per line:

```
{"id": 123, "condition": "same|flip1|flip2|flip3", "title": "...", "text": "..."}
```

WELFake is released under CC BY 4.0 (Verma et al., DOI 10.5281/zenodo.4561253). These rewrites are derived
from it and keep the same licence. Rewritten *fake* articles still contain false claims: they exist only to
test classifiers.

## Generation notes

- **Coverage:** 600 articles × 4 conditions = 2,400 rewrites, in 24 files. Every file passes
  `scripts/validate_rewrites.py` with 0 errors. The remaining warnings were checked by hand: almost all are numbers that only
  appeared in dropped boilerplate (bylines, timestamps, share counters, Twitter handles) or neutral rewrites that are
  shorter than the original.
- **Written by:** Claude, in parallel sessions that each handled 2 chunks from the same fixed prompt.
- **Judgement calls applied across files** (worth stating in the report):
  - Boilerplate is removed in *every* condition, including `same`: bylines, dates, share counters, ads, author bios,
    newsletter footers, hashtags and @handles. Agency attributions ("told Reuters") become "said" or "a news report".
  - Sentences cut off by the 300-word truncation are dropped or ended without adding facts. Obvious scraping gaps and
    typos were repaired minimally (e.g. "50,00" → "50,000" in 10977, "$11. 6 million" → "$11.6 million").
  - Offensive language: kept at the original level in `same`; insults in the author's own voice are removed in the
    neutral flips (fake articles); sensational flips (real articles) never add slurs or attacks on groups.
  - Quotations stay word for word, with a few deliberate exceptions in the neutral flips where a quote contains a slur
    (e.g. 12158, 17420, 58991) or a long quoted passage was turned into indirect speech (63151). There the content is
    kept as reported speech. The NLI check in notebook 03b measures whether content survived.
