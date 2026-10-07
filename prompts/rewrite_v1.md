# Style-rewrite prompt, v1

Used to create every rewrite in `rewrites/`. The model sees the article after `strip_source_markers`
(no agency tags, publisher suffixes, media tags, image credits or URLs), truncated to about 300 words.

For each article there are four rewrites:

| `condition` | Real article (label 0) | Fake article (label 1) |
|---|---|---|
| `same` | paraphrase, keep its neutral news tone | paraphrase, keep its sensational tone |
| `flip1` | mildly sensational | mildly neutral |
| `flip2` | clearly sensational | fully neutral |
| `flip3` | extremely sensational, tabloid/clickbait | formal wire-service register |

---

## Instructions given to the model

You are rewriting a news article to change **only its writing style**. The article's content must stay
exactly the same. These rewrites are used to test whether fake-news classifiers judge content or tone.

### Content rules (all conditions)
1. Keep **every** factual claim, event, named person, organisation, place, number and date. Do not drop any.
2. Keep direct quotations **word for word** inside quotation marks.
3. **Add nothing new:** no new facts, events, numbers, sources, quotes, background or context.
4. **Do not correct, hedge or debunk.** If the article states something as fact, the rewrite states it as fact.
   Do not add words like "allegedly", "claimed", "unverified" or "according to the author" that are not in the original.
5. **Do not remove or soften claims either.** Keep strong claims strong in content, even when the wording calms down.
6. Do not add agency names, datelines, bylines, publication names, image credits, URLs, hashtags or `[VIDEO]`-style tags.
7. Keep the length within about ±15% of the original body. Write in English. Write the title and the body.
8. Drop leftover web boilerplate that is not part of the story: bylines ("By Jane Doe"), share counters
   ("10 Shares"), "Email", category lists, timestamps, a leading "- ", and a title repeated at the start of the body.
   Drop it in **every** condition, including `same`.
9. Typos and missing apostrophes in the input (e.g. "Brazil s") may be corrected; they are scraping artefacts.

### Target styles

**Same style (`same`).** Reword sentences and change sentence structure, but keep the tone, register and
emotional intensity of the original. A calm article stays calm; an angry one stays angry.

**Sensational, for real articles**
- `flip1` (mild): a few emotive words and intensifiers ("stunning", "major"), a punchier headline.
- `flip2` (clear): emotive and judgemental vocabulary, short punchy sentences, a rhetorical question or two,
  an exclamation mark, a dramatic headline.
- `flip3` (extreme): tabloid/clickbait register: an all-caps or shouting headline, heavy emotive language,
  direct address to the reader ("You won't believe..."), several exclamation marks, outraged or breathless tone.

  Emotion may be *expressed* ("This is outrageous!") but no new *facts* may be asserted.

**Neutral, for fake articles**
- `flip1` (mild): remove insults, exclamations and capitalised shouting; tone down the strongest emotive words.
- `flip2` (fully neutral): plain, impersonal news prose; no emotive or judgemental words, no rhetorical
  questions, no exclamation marks, no direct address to the reader.
- `flip3` (wire service): formal wire-service register: inverted-pyramid order (most important claim first),
  past tense, third person, short factual sentences, a sober descriptive headline in sentence case.

  The claims stay asserted as fact (rule 4); only the wording becomes neutral.

### Output format
One JSON object per line, no other text:

```
{"id": <article id>, "condition": "same|flip1|flip2|flip3", "title": "...", "text": "..."}
```
