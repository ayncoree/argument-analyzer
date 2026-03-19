"""
graph.py — Upgraded argument graph builder.

Improvements over v1:
- Nodes carry full metadata (label, short_label, type, color, size)
- Edges carry label, style, and color
- Smart layout: premises on left half, rebuttals on right, undercutters below
- Short labels generated automatically to avoid visual clutter
- Pyvis-compatible output (for interactive rendering) alongside networkx format
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
COLORS = {
    "conclusion":  "#5B8FF9",   # calm blue
    "premise":     "#5AD8A6",   # teal-green
    "rebuttal":    "#F4664A",   # red-orange
    "undercutter": "#FAAD14",   # amber
    "fallacy":     "#C37FFF",   # purple
}

SIZE = {
    "conclusion":  45,
    "premise":     30,
    "rebuttal":    25,
    "undercutter": 25,
    "fallacy":     20,
}

EDGE_COLOR = {
    "support":      "#5AD8A6",
    "rebuttal":     "#F4664A",
    "undercutter":  "#FAAD14",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _short_label(text: str, max_words: int = 8) -> str:
    """Truncate label to at most *max_words* words, appending '…' if needed."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + " …"


def _layout_position(
    node_type: str,
    index: int,
    total: int,
) -> Tuple[float, float]:
    """
    Assign a 2-D position based on node type.

    Layout:
        Conclusion  →  (0, 0)          centre
        Premises    →  left column, spread vertically
        Rebuttals   →  right column, spread vertically
        Undercutters→  below, spread horizontally
        Fallacies   →  top, spread horizontally
    """
    spread = max(1, total - 1)

    if node_type == "conclusion":
        return 0.0, 0.0

    if node_type == "premise":
        y = (index / spread * 2) - 1 if spread > 0 else 0.0
        return -2.0, y

    if node_type == "rebuttal":
        y = (index / spread * 2) - 1 if spread > 0 else 0.0
        return 2.0, y

    if node_type == "undercutter":
        x = (index / spread * 2) - 1 if spread > 0 else 0.0
        return x, -2.5

    if node_type == "fallacy":
        x = (index / spread * 2) - 1 if spread > 0 else 0.0
        return x, 2.5

    return 0.0, 0.0


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_argument_graph(
    conclusion: Optional[str],
    premises: List[str],
    objections: List[Dict],
    fallacies: Optional[List[Dict]] = None,
) -> Dict:
    """
    Build a rich argument graph.

    Parameters
    ----------
    conclusion  : The main conclusion text (or None).
    premises    : List of premise strings.
    objections  : List of objection dicts from detect_counter_arguments().
    fallacies   : Optional list of fallacy dicts from detect_all_fallacies().

    Returns
    -------
    {
        "nodes": [ {id, label, short_label, type, color, size, x, y} ],
        "edges": [ {from, to, type, style, color, label} ],
    }
    """
    nodes: List[Dict] = []
    edges: List[Dict] = []

    # Type-indexed counts for layout
    type_counts: Dict[str, int] = {}

    def _next_idx(node_type: str) -> int:
        idx = type_counts.get(node_type, 0)
        type_counts[node_type] = idx + 1
        return idx

    # ── Conclusion ────────────────────────────────────────────────────────
    if conclusion:
        nodes.append({
            "id": "C",
            "label": conclusion,
            "short_label": _short_label(conclusion),
            "type": "conclusion",
            "color": COLORS["conclusion"],
            "size": SIZE["conclusion"],
            "x": 0.0,
            "y": 0.0,
        })

    # ── Premises ─────────────────────────────────────────────────────────
    n_premises = len(premises)
    for i, p in enumerate(premises):
        pid = f"P{i}"
        x, y = _layout_position("premise", i, n_premises)
        nodes.append({
            "id": pid,
            "label": p,
            "short_label": _short_label(p),
            "type": "premise",
            "color": COLORS["premise"],
            "size": SIZE["premise"],
            "x": x,
            "y": y,
        })
        if conclusion:
            edges.append({
                "from": pid,
                "to": "C",
                "type": "support",
                "style": "solid",
                "color": EDGE_COLOR["support"],
                "label": "supports",
            })

    # ── Objections ────────────────────────────────────────────────────────
    rebuttals  = [o for o in objections if o.get("type") == "rebuttal"]
    undercuts  = [o for o in objections if o.get("type") == "undercutter"]

    n_rebuttals  = len(rebuttals)
    n_undercuts  = len(undercuts)

    for i, o in enumerate(rebuttals):
        oid = f"R{i}"
        x, y = _layout_position("rebuttal", i, n_rebuttals)
        nodes.append({
            "id": oid,
            "label": o["sentence"],
            "short_label": _short_label(o["sentence"]),
            "type": "rebuttal",
            "color": COLORS["rebuttal"],
            "size": SIZE["rebuttal"],
            "x": x,
            "y": y,
        })
        if conclusion:
            edges.append({
                "from": oid,
                "to": "C",
                "type": "rebuttal",
                "style": "dashed",
                "color": EDGE_COLOR["rebuttal"],
                "label": "rebuts",
            })

    for i, o in enumerate(undercuts):
        oid = f"U{i}"
        x, y = _layout_position("undercutter", i, n_undercuts)

        # Try to match to the right premise node
        target_id = "C"    # fallback to conclusion
        if premises:
            target_text = o.get("target", "")
            for j, p in enumerate(premises):
                if p == target_text or target_text in p:
                    target_id = f"P{j}"
                    break
            else:
                target_id = "P0"   # default to first premise

        nodes.append({
            "id": oid,
            "label": o["sentence"],
            "short_label": _short_label(o["sentence"]),
            "type": "undercutter",
            "color": COLORS["undercutter"],
            "size": SIZE["undercutter"],
            "x": x,
            "y": y,
        })
        edges.append({
            "from": oid,
            "to": target_id,
            "type": "undercutter",
            "style": "dashed",
            "color": EDGE_COLOR["undercutter"],
            "label": "undercuts",
        })

    # ── Fallacies (optional overlay) ─────────────────────────────────────
    n_fallacies = len(fallacies) if fallacies else 0
    for i, f in enumerate(fallacies or []):
        fid = f"F{i}"
        x, y = _layout_position("fallacy", i, n_fallacies)
        nodes.append({
            "id": fid,
            "label": f"[{f['type']}] {f['sentence']}",
            "short_label": f"⚠ {f['type']}",
            "type": "fallacy",
            "color": COLORS["fallacy"],
            "size": SIZE["fallacy"],
            "x": x,
            "y": y,
        })
        # Connect fallacy to conclusion or the sentence's premise
        edges.append({
            "from": fid,
            "to": "C",
            "type": "fallacy",
            "style": "dotted",
            "color": COLORS["fallacy"],
            "label": "fallacy",
        })

    return {"nodes": nodes, "edges": edges}
