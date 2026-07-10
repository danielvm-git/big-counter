#!/usr/bin/env python3
"""Generate OKF viz.html for docs/bcp-ruler/ — self-contained, no external deps beyond pyyaml."""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SCRIPTS_DIR = Path(__file__).resolve().parent
BUNDLE_ROOT = SCRIPTS_DIR.parent / "docs" / "bcp-ruler"
_LINK_RE = re.compile(r"\]\(([^)\s]+\.md)(?:#[A-Za-z0-9_\-]*)?\)")
_INDEX_NAME = "index.md"

_TYPE_PALETTE = {
    "Methodology": "#ef4444",
    "Dimension": "#3b82f6",
    "Concept": "#10b981",
}
_DEFAULT_NODE_COLOR = "#94a3b8"


@dataclass
class Concept:
    id: str
    type: str
    title: str
    description: str
    tags: list[str]
    body: str
    links_to: list[str] = field(default_factory=list)

    def to_node(self) -> dict[str, Any]:
        color = _TYPE_PALETTE.get(self.type, _DEFAULT_NODE_COLOR)
        return {
            "data": {
                "id": self.id,
                "label": self.title or self.id,
                "type": self.type,
                "description": self.description,
                "tags": self.tags,
                "color": color,
                "size": 30 + min(60, len(self.body) // 200),
            }
        }


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}, text
    fm_text = "\n".join(lines[1:end_idx])
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return {}, text
    if not isinstance(fm, dict):
        return {}, text
    body = "\n".join(lines[end_idx + 1 :])
    if body.startswith("\n"):
        body = body[1:]
    return fm, body


def _extract_links(body: str, doc_dir: Path, bundle_root: Path) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    bundle_root_resolved = bundle_root.resolve()
    for m in _LINK_RE.finditer(body):
        target = m.group(1)
        if "://" in target:
            continue
        # Resolve absolute (bundle-relative) links starting with /
        if target.startswith("/"):
            target_path = bundle_root_resolved / target.lstrip("/")
        else:
            target_path = doc_dir / target
        try:
            resolved = target_path.resolve().relative_to(bundle_root_resolved)
        except ValueError:
            continue
        rel = resolved.as_posix()
        if rel.endswith(".md"):
            rel = rel[:-3]
        if rel and rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out


def _walk_concepts(bundle_root: Path) -> list[Concept]:
    concepts: list[Concept] = []
    for md_path in sorted(bundle_root.rglob("*.md")):
        if md_path.name == _INDEX_NAME:
            continue
        rel = md_path.relative_to(bundle_root).with_suffix("")
        concept_id = "/".join(rel.parts)
        try:
            fm, body = _parse_frontmatter(md_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        tags = fm.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        concept = Concept(
            id=concept_id,
            type=str(fm.get("type") or "Unknown"),
            title=str(fm.get("title") or concept_id),
            description=str(fm.get("description") or ""),
            tags=[str(t) for t in tags],
            body=body or "",
            links_to=_extract_links(body or "", md_path.parent, bundle_root),
        )
        concepts.append(concept)
    return concepts


def _build_graph(concepts: list[Concept]) -> dict[str, Any]:
    ids = {c.id for c in concepts}
    nodes = [c.to_node() for c in concepts]
    edges: list[dict[str, Any]] = []
    seen_edges: set[tuple[str, str]] = set()
    for c in concepts:
        for target in c.links_to:
            if target == c.id or target not in ids:
                continue
            key = (c.id, target)
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append(
                {
                    "data": {
                        "id": f"{c.id}__{target}",
                        "source": c.id,
                        "target": target,
                    }
                }
            )
    bodies = {c.id: c.body for c in concepts}
    types = sorted({c.type for c in concepts})
    return {
        "nodes": nodes,
        "edges": edges,
        "bodies": bodies,
        "types": types,
        "palette": _TYPE_PALETTE,
    }


def main() -> None:
    bundle_name = "BCP Plus Ruler"
    concepts = _walk_concepts(BUNDLE_ROOT)
    graph = _build_graph(concepts)

    template = (SCRIPTS_DIR / "okf_viz_template.html").read_text(encoding="utf-8")
    css = (SCRIPTS_DIR / "okf_viz.css").read_text(encoding="utf-8")
    js = (SCRIPTS_DIR / "okf_viz.js").read_text(encoding="utf-8")

    html = (
        template.replace("/*__VIZ_CSS__*/", css)
        .replace("/*__VIZ_JS__*/", js)
        .replace("__BUNDLE_NAME__", json.dumps(bundle_name))
        .replace("__BUNDLE_DATA__", json.dumps(graph))
    )

    out_path = BUNDLE_ROOT / "viz.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} ({len(html.encode('utf-8'))} bytes)")
    print(f"  {len(concepts)} concepts, {len(graph['edges'])} edges")


if __name__ == "__main__":
    main()
