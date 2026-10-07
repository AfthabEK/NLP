# Augmentation rewrites (training set)

Style-flipped rewrites of 500 WELFake **training** articles (250 real, 250 fake, sampled in notebook 04a), used by
notebook 04b to train the augmentation defense. Same prompt as the test-set rewrites
([`../prompts/rewrite_v1.md`](../prompts/rewrite_v1.md)), but only two conditions per article:

- `flip2`: real articles written sensationally, fake articles written neutrally
- `flip3`: the same at extreme intensity (tabloid vs. wire-service register)

Every rewrite keeps its article's original label, so the models see fake news in a calm tone and real news in a loud
one.

- **Contents:** 20 files, `chunk_XX.jsonl`, rows `{"id", "condition", "title", "text"}`: 996 rewrites of 498 articles.
- **Validation:** every file passes `scripts/validate_rewrites.py ... flip2,flip3` with 0 errors, apart from the two
  skipped articles below.
- **Skipped:** two articles were left out deliberately:
  - 13257: the agent could not rewrite it faithfully.
  - 12084: fake satire with sexual content involving child characters.
- **Judgement calls:** the same as for `rewrites/` (see its README). Boilerplate is removed; the author's own insults
  are removed in the neutral rewrites; quotations stay word for word except slurs, which are reported as speech;
  sensational rewrites never add slurs or attacks on groups.

WELFake is CC BY 4.0; these derived rewrites keep the same licence.
