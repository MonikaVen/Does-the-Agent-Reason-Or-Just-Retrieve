from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Any


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9.+_/-]+", (text or "").lower())


def token_f1(prediction: str, gold: str) -> float:
    pred = tokenize(prediction)
    ref = tokenize(gold)
    if not pred and not ref:
        return 1.0
    if not pred or not ref:
        return 0.0
    overlap = len(set(pred) & set(ref))
    if overlap == 0:
        return 0.0
    precision = overlap / len(set(pred))
    recall = overlap / len(set(ref))
    return round(2 * precision * recall / (precision + recall), 4)


def exact_ci(prediction: str, accept: list[str] | str | None) -> float:
    pred = (prediction or "").strip().lower()
    if isinstance(accept, str):
        items = [accept]
    else:
        items = [a for a in (accept or []) if a]
    normalized = []
    for item in items:
        if isinstance(item, (list, tuple)):
            normalized.extend(str(x) for x in item)
        else:
            normalized.append(str(item))
    uniq = sorted({a.strip().lower() for a in normalized if str(a).strip()}, key=len, reverse=True)
    if not uniq:
        return 0.0
    # Multi-answer keys: fraction of accepted items mentioned.
    if len(uniq) >= 3:
        hits = sum(1 for item in uniq if item in pred)
        return round(hits / len(uniq), 4)
    for item in uniq:
        if item and item in pred:
            return 1.0
    return 0.0


def yes_no_match(prediction: str, expect_yes: bool) -> float:
    text = (prediction or "").strip().lower()
    yes = bool(re.search(r"\b(yes|true|correct)\b", text))
    no = bool(re.search(r"\b(no|false|incorrect)\b", text))
    if expect_yes:
        return 1.0 if yes and not no else 0.0
    return 1.0 if no and not yes else 0.0


def ollama_generate(
    *,
    model: str,
    system: str,
    user: str,
    base_url: str = "http://127.0.0.1:11434",
    num_predict: int = 512,
    temperature: float = 0.1,
) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": num_predict},
    }
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama call failed: {exc}") from exc
    return ((data.get("message") or {}).get("content") or "").strip()


def scenario_row(
    *,
    dataset: str,
    scenario: str,
    model: str,
    score: float,
    status: str = "completed",
    detail: str = "",
    prediction: str = "",
    gold: str = "",
) -> dict[str, Any]:
    return {
        "dataset": dataset,
        "scenario": scenario,
        "model": model,
        "score": round(float(score), 4),
        "status": status,
        "detail": detail,
        "prediction": prediction[:500],
        "gold": gold[:500],
    }
