# Project plan: Style vs. Substance in Fake News Detection

**Working title:** *Do Fake News Classifiers Learn Truth or Tone? A Style-Attack Study of TF‑IDF vs. DistilBERT*

## 1. Problem and research questions
Fake news classifiers score highly on benchmark datasets. In many datasets, though, fake and real news differ in
**writing style** (sensational vs. neutral wire-service tone), and a model can score well just by learning that
style. We test this by having an LLM rewrite articles so the style flips while the content stays the same, then
measuring how far each model's accuracy falls.

- **RQ1:** How much do TF‑IDF + LR and DistilBERT rely on style? That is, how far does accuracy drop when style is flipped but content is kept?
- **RQ2:** Does the drop grow with style intensity, and does it differ between the two models?
- **RQ3:** What does each model rely on? Which features or tokens drive its predictions before and after the attack?
- **RQ4:** Which defense restores robustness more cheaply: LLM-rewrite augmentation or simple style normalisation?

**Positioning:** this builds on SheepDog (Wu & Hooi, KDD 2024), which introduced LLM style attacks and
augmentation-based defenses. Our contributions are:
- a classical vs. transformer comparison under the attack
- a dose–response analysis of style intensity
- an interpretability analysis of which features break
- a comparison of LLM augmentation against a zero-cost normalisation defense

## 2. Data
| Role | Dataset | Notes |
|---|---|---|
| Main | **WELFake** (~72k, title + text, binary) | Zenodo / Hugging Face mirror |
| Showcase (optional) | **ISOT** (~45k) | Its "(Reuters)" dateline is a known style shortcut |
| Comparison (optional) | **FakeNewsNet** (PolitiFact / GossipCop) | The datasets SheepDog used |

The synthetic Kaggle dataset from Phase 1 is dropped.

**Preprocessing:**
- Remove empty texts, articles under 50 words, non-English articles, duplicates and texts that appear with both labels.
- Keep a stratified working subset of 30k articles.
- Make a stratified **70/15/15 split by article ID** with seed 42. Every rewrite stays in its source article's split.

## 3. Method
### 3.1 Classifiers
- **TF‑IDF + LR:** word 1–2-grams, sublinear TF, with C tuned on the validation set.
- **DistilBERT:** input is `title [SEP] text`, max 256–512 tokens, 2–3 epochs, learning rate around 2e‑5, early stopping on validation, 3 seeds.

### 3.2 Style attack (test subset)
| Condition | What it does | Purpose |
|---|---|---|
| Original | Unchanged; truncated to the same length as the rewrites | Clean accuracy |
| Same-style paraphrase | Rewrite that keeps the original tone | Control for "LLM-written text" effects |
| Flipped style, levels 1–3 | Fake → neutral wire-service tone; real → sensational tone, at mild, moderate and extreme intensity | The attack, plus the dose–response curve |

- **LLM:** Claude, generating rewrites in Claude Code sessions from a fixed, versioned prompt. Rewrites are saved to Drive as parquet with the article `id`, condition and level.
- **Prompt rule:** change tone only. Every claim, number, name, date and quote must be kept.
- **Automatic filter:** a DeBERTa‑MNLI model checks entailment in both directions between original and rewrite. Rewrites that fail are discarded.
- **Human audit:** 100 random pairs, each rated by 2 annotators, reporting the share where the label was preserved and Cohen's κ.

### 3.3 Defenses
1. **Style normalisation (zero cost):**
   - lowercase the text
   - strip exclamation marks and repeated punctuation
   - mask datelines and agency names
   - optionally mask named entities

   Then retrain both models.
2. **LLM augmentation:** add style-flipped rewrites of training articles, with their original labels, and retrain.
3. **Combined:** normalisation plus augmentation.

### 3.4 Interpretability
- **LR:** compare the top‑weighted n‑grams for each class across the clean, normalised and augmented models.
- **DistilBERT:** use Integrated Gradients (Captum) on correct predictions that flip after the attack.

## 4. Evaluation
- **Clean performance:** accuracy, macro F1, per-class precision and recall, ROC‑AUC, confusion matrix.
- **Robustness:**
  - accuracy drop from Original to Flipped
  - the **style effect**, defined as the Flipped drop minus the Same-style drop
  - **flip rate**: the share of correct predictions that become wrong
  - all of the above **broken down by class**
- **Dose–response:** accuracy against intensity level for each model.
- **Defense value:** robust accuracy recovered vs. clean accuracy lost, and the cost of each defense.
- **Significance:** McNemar's test on paired predictions, plus bootstrap confidence intervals on the drops.

## 5. Stages and timeline
| Week | Stage | Deliverables |
|---|---|---|
| 1 | 1. Data | Notebook 01: loading, EDA, style cues, splits |
| 2 | 2. Baseline | Notebook 01: TF‑IDF + LR, top features |
| 3 | 3. Transformer | Notebook 02: DistilBERT (3 seeds), clean comparison |
| 3–4 | 4a. Attack generation | Rewrite prompts, rewrites, NLI filter, human audit |
| 5 | 4b. Attack evaluation | Notebook 03: drops, style effect, dose–response, Integrated Gradients |
| 6 | 4c. Defenses | Notebook 04: normalisation and augmentation |
| 7 | 5. Analysis + demo | Final figures; demo showing one article in two styles with both models' predictions |
| 8 | Report | Final report, slides, cleaned repository |

## 6. Roles
| Role | Responsibility |
|---|---|
| Data lead | Loading, EDA, cleaning, splits, normalisation defense |
| Classical lead | TF‑IDF + LR, feature analysis, significance tests |
| Transformer lead | DistilBERT, Integrated Gradients |
| Attack lead | Rewrite prompts and generation, NLI filter, augmentation set |
| Evaluation + demo lead | Metrics harness, plots, demo, report integration |

Everyone helps with the human audit.

## 7. Risks and mitigations
| Risk | Mitigation |
|---|---|
| Rewrites change the facts, so the label is wrong | Strict prompt, NLI filter, human audit, report the preservation rate |
| The drop comes from text being LLM-written rather than the style flip | Same-style paraphrase control |
| Scores near the ceiling on WELFake | Focus on robustness metrics; ISOT / FakeNewsNet as harder settings |
| Leakage between an article and its rewrites | Split by article ID before any rewriting |
| Length mismatch between originals and rewrites | Truncate originals to the rewrite input length; evaluate originals in truncated form |
