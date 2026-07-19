#!/usr/bin/env python3
"""Validate, rank, and render a weapon-reference candidate manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED = ("id", "title", "image_url", "landing_url", "source", "license", "tags")
SOURCE_TIER = {
    "cleveland museum of art": 3,
    "the metropolitan museum of art": 3,
    "metropolitan museum of art": 3,
    "smithsonian": 3,
    "wikimedia commons": 3,
    "rijksmuseum": 3,
    "kaykit": 2,
    "game icons": 2,
    "open images": 1,
    "od-weapondetection": 1,
}
LICENSE_SCORE = {
    "cc0": 3,
    "public domain": 3,
    "cc by": 2,
    "cc-by": 2,
    "cc by-sa": 1,
    "cc-by-sa": 1,
}


def load_candidates(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("candidates")
    if not isinstance(data, list) or not data:
        raise ValueError("input must be a non-empty list or an object with candidates[]")
    seen: set[str] = set()
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"candidate {index} must be an object")
        missing = [field for field in REQUIRED if not item.get(field)]
        if missing:
            raise ValueError(f"candidate {index} missing: {', '.join(missing)}")
        if not isinstance(item["tags"], list):
            raise ValueError(f"candidate {item['id']} tags must be a list")
        candidate_id = str(item["id"])
        if candidate_id in seen:
            raise ValueError(f"duplicate candidate id: {candidate_id}")
        seen.add(candidate_id)
    return data


def normalized_set(values: list[Any]) -> set[str]:
    return {str(value).strip().casefold() for value in values if str(value).strip()}


def contains_score(value: str, mapping: dict[str, int]) -> int:
    normalized = value.casefold()
    return max((score for key, score in mapping.items() if key in normalized), default=0)


def rank(candidate: dict[str, Any], query_tags: set[str]) -> tuple[int, int, int, str]:
    tags = normalized_set(candidate.get("tags", []))
    overlap = len(tags & query_tags)
    verified = 1 if candidate.get("license_verified") is True else 0
    source = contains_score(str(candidate.get("source", "")), SOURCE_TIER)
    license_score = contains_score(str(candidate.get("license", "")), LICENSE_SCORE)
    score = overlap * 10 + verified * 5 + source * 2 + license_score
    return score, overlap, verified, str(candidate["id"])


def markdown(candidates: list[dict[str, Any]]) -> str:
    blocks = ["# 武器参考候选"]
    for item in candidates:
        image = item.get("thumbnail_url") or item["image_url"]
        reasons = "；".join(item.get("match_reasons", [])) or "待人工判断"
        strengths = "、".join(item.get("reference_strength", [])) or "待标注"
        tags = "、".join(map(str, item.get("tags", [])))
        verified = "已核验" if item.get("license_verified") is True else "未核验"
        blocks.extend(
            [
                f"## {item['id']}｜{item['title']}",
                f"![{item['id']}]({image})",
                f"- 来源：{item['source']}｜{item['landing_url']}",
                f"- 许可证：{item['license']}（{verified}）",
                f"- 标签：{tags}",
                f"- 匹配理由：{reasons}",
                f"- 最适合参考：{strengths}",
            ]
        )
    return "\n\n".join(blocks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="candidate JSON file")
    parser.add_argument("--query-tags", default="", help="comma-separated normalized query tags")
    parser.add_argument("--json-out", type=Path, help="write ranked JSON")
    parser.add_argument("--markdown-out", type=Path, help="write Markdown candidate gallery")
    args = parser.parse_args()

    candidates = load_candidates(args.input)
    query_tags = normalized_set(args.query_tags.split(","))
    ranked = sorted(candidates, key=lambda item: rank(item, query_tags), reverse=True)
    for item in ranked:
        score, overlap, verified, _ = rank(item, query_tags)
        item["ranking"] = {"score": score, "tag_overlap": overlap, "license_verified": bool(verified)}

    payload = {"query_tags": sorted(query_tags), "candidates": ranked}
    if args.json_out:
        args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.write_text(markdown(ranked), encoding="utf-8")
    if not args.json_out and not args.markdown_out:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

