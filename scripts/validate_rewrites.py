"""Check a rewrite file against its input chunk.

    python scripts/validate_rewrites.py INPUT_CHUNK.jsonl REWRITES.jsonl

Errors (exit code 1): malformed lines, unknown ids/conditions, missing or duplicate (id, condition) pairs,
empty fields, URLs or agency tags, body length far from the original.
Warnings: numbers or long direct quotations from the original that do not appear in a rewrite, and
moderate length drift. Each warning should be checked by hand and fixed if content was lost.
"""
import json
import re
import sys

CONDITIONS = ("same", "flip1", "flip2", "flip3")
HARD_RATIO = (0.6, 1.5)
SOFT_RATIO = (0.8, 1.25)
URL = re.compile(r"https?://|www\.|pic\.twitter\.com", re.I)
AGENCY = re.compile(r"\((?:Reuters|AP|AFP|Bloomberg)\)", re.I)
QUOTE = re.compile(r"[“\"]([^”\"]{25,}?)[”\"]")
NUMBER = re.compile(r"\d[\d,.]*\d|\d")


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def numbers(s):
    return {re.sub(r"[,\s]", "", n).rstrip(".") for n in NUMBER.findall(re.sub(r"(\d), (\d{3})", r"\1,\2", s))}


def main(input_path, output_path):
    articles = {}
    with open(input_path) as f:
        for line in f:
            if line.strip():
                a = json.loads(line)
                articles[a["id"]] = a
    errors, warnings, seen = [], [], set()
    with open(output_path) as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {n}: invalid JSON ({e})")
                continue
            key = (r.get("id"), r.get("condition"))
            if set(r) != {"id", "condition", "title", "text"}:
                errors.append(f"line {n}: keys must be id, condition, title, text (got {sorted(r)})")
                continue
            if r["id"] not in articles:
                errors.append(f"line {n}: id {r['id']} is not in the input chunk")
                continue
            if r["condition"] not in CONDITIONS:
                errors.append(f"line {n}: unknown condition {r['condition']!r}")
                continue
            if key in seen:
                errors.append(f"line {n}: duplicate {key}")
            seen.add(key)
            if not r["title"].strip() or not r["text"].strip():
                errors.append(f"{key}: empty title or text")
                continue
            if URL.search(r["title"] + r["text"]) or AGENCY.search(r["title"] + r["text"]):
                errors.append(f"{key}: contains a URL or agency tag")
            src = articles[r["id"]]
            ratio = len(r["text"].split()) / max(len(src["text"].split()), 1)
            if not HARD_RATIO[0] <= ratio <= HARD_RATIO[1]:
                errors.append(f"{key}: body length ratio {ratio:.2f} (allowed {HARD_RATIO})")
            elif not SOFT_RATIO[0] <= ratio <= SOFT_RATIO[1]:
                warnings.append(f"{key}: body length ratio {ratio:.2f}")
            out_norm = norm(r["title"] + " " + r["text"])
            missing_nums = numbers(src["title"] + " " + src["text"]) - numbers(r["title"] + " " + r["text"])
            if missing_nums:
                warnings.append(f"{key}: numbers not found: {sorted(missing_nums)[:8]}")
            for q in QUOTE.findall(src["text"]):
                if norm(q) not in out_norm:
                    warnings.append(f"{key}: quote not found verbatim: \"{q[:60]}...\"")
    for aid in articles:
        for c in CONDITIONS:
            if (aid, c) not in seen:
                errors.append(f"missing ({aid}, {c})")
    print(f"{len(seen)} rewrites checked for {len(articles)} articles: {len(errors)} errors, {len(warnings)} warnings")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARNING", w)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
