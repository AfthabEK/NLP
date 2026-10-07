# Do Fake News Classifiers Learn Truth or Tone?

NLP course project (Group 8, BITS Pilani Hyderabad). We compare **TF‑IDF + Logistic Regression** with
**DistilBERT** for fake news detection. Then we test how much each model relies on *writing style*, using
**LLM style attacks**: fake articles rewritten in a neutral wire-service tone, and real articles rewritten in a
sensational tone, with the facts unchanged. See [`docs/project_plan.md`](docs/project_plan.md) for the full plan.

## Notebooks

| # | Notebook | Runtime | Status |
|---|---|---|---|
| 01 | [`01_data_and_baseline.ipynb`](notebooks/01_data_and_baseline.ipynb): WELFake loading, cleaning, EDA, style cues, splits, TF‑IDF + LR baseline | CPU | done |
| 02 | [`02_distilbert.ipynb`](notebooks/02_distilbert.ipynb): DistilBERT fine-tuning (3 seeds), comparison with TF‑IDF, McNemar test | GPU (T4) | done |
| 03a | [`03a_attack_sample.ipynb`](notebooks/03a_attack_sample.ipynb): sample 600 test articles, truncate, strip source markers, export for rewriting | CPU | done |
| 03b | [`03b_style_attack.ipynb`](notebooks/03b_style_attack.ipynb): NLI content check, accuracy by condition, effect decomposition, flip rates, dose–response | GPU (T4) | ready |
| 04 | Defenses: style normalisation vs. rewrite augmentation | GPU | planned |
| 05 | Final analysis, figures, demo | CPU | planned |

## Running on Google Colab

1. Open the notebook in Colab. Either upload it, or open it from Google Drive with **Open with → Google Colaboratory**.
2. For GPU notebooks: **Runtime → Change runtime type → T4 GPU**.
3. **Runtime → Run all** and approve the Google Drive prompt.
4. On a phone, tap ▶ on the keep-alive player in the first cell. It loops a near-silent sound so the browser doesn't suspend the tab during long runs.

Every notebook reads and writes `MyDrive/NLP_style_attack/`:

```
NLP_style_attack/
├── data/      train.parquet, val.parquet, test.parquet (+ rewrites later)
├── models/    fitted models
├── results/   JSON / CSV metrics
└── figures/   plots
```

Later notebooks depend on the splits made in notebook 01, so run them in order.

## Dataset

**WELFake**: 72,134 news articles (title, text, label), merged from Kaggle, McIntire, Reuters and BuzzFeed Political.
Source: Zenodo, DOI [10.5281/zenodo.4561253](https://doi.org/10.5281/zenodo.4561253) (CC BY 4.0), mirrored at
[`davanstrien/WELFake`](https://huggingface.co/datasets/davanstrien/WELFake).

> **Label caveat:** the WELFake documentation says `0 = fake, 1 = real`, but the published data appears to use
> the opposite convention (Reuters wire stories are labelled `0`). Notebook 01 infers the mapping from the data
> and stores an unambiguous column `fake` (1 = fake, 0 = real), which all later notebooks use.

## Repository layout

| Path | Contents |
|---|---|
| `notebooks/` | Colab notebooks, run in order |
| `src/fakestyle/` | Shared code the notebooks download from GitHub (text truncation, source-marker stripping) |
| `tests/` | Unit tests for `src/` (`python -m pytest tests`) |
| `scripts/` | `validate_rewrites.py`: checks a rewrite file against its input chunk |
| `prompts/` | The fixed LLM rewrite prompt |
| `rewrites/` | Generated style rewrites (see its README) |
| `docs/` | Project plan |
