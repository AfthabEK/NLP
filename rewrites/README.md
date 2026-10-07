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
