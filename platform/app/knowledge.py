from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .store import DATA_DIR


class KnowledgeService:
    def __init__(self, path: Path | None = None) -> None:
        kb_path = path or (DATA_DIR / "knowledge.json")
        self.corpus = json.loads(kb_path.read_text())

    def search(self, question: str, corpus_tags: list[str] | None = None, top_k: int = 4) -> dict[str, Any]:
        tags = {tag.lower() for tag in (corpus_tags or [])}
        tokens = {token.lower() for token in re.findall(r"[a-zA-Z0-9.+-]+", question) if len(token) > 2}
        scored = []
        for passage in self.corpus["passages"]:
            hay = " ".join(
                [
                    passage["text"],
                    passage["category"],
                    " ".join(passage.get("corpus_tags") or []),
                    passage["source_id"],
                ]
            ).lower()
            tag_score = len(tags.intersection({t.lower() for t in passage.get("corpus_tags") or []}))
            token_score = sum(1 for token in tokens if token in hay)
            score = 0.15 * tag_score + 0.12 * token_score
            if passage["category"] in {"detection", "procedural"}:
                score += 0.05
            scored.append((score, passage))
        scored.sort(key=lambda item: item[0], reverse=True)
        passages = []
        for score, passage in scored[: max(1, top_k)]:
            passages.append(
                {
                    "passage_id": passage["passage_id"],
                    "source_id": passage["source_id"],
                    "source_version": passage["source_version"],
                    "category": passage["category"],
                    "text": passage["text"],
                    "score": round(min(0.99, 0.45 + score), 2),
                }
            )
        return {"passages": passages, "index_version": self.corpus["index_version"]}
