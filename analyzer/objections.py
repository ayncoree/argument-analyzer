"""
objections.py — Next-Gen Counter-Argument & Rebuttal Generator

Features:
- Discourse-based rebuttal detection
- Premise-based undercutter detection
- NEW: "Devil's Advocate" Generator (Automatic rebuttal suggestions)
"""

from __future__ import annotations
import re
from typing import Dict, List, Optional, Set, Tuple

# ──────────────────────────────────────────────────────────────────────────────
# Rebuttal markers — each maps to a specific explanation
# ──────────────────────────────────────────────────────────────────────────────

REBUTTAL_MARKER_EXPLANATIONS: List[Tuple[str, str]] = [
    ("however",              "Introduces a direct contrast that opposes the preceding claim."),
    ("but",                  "Signals an objection or exception to the argument just made."),
    ("although",             "Concedes part of the argument while challenging its overall validity."),
    ("yet",                  "Acknowledges the previous point but asserts a conflicting conclusion."),
    ("on the other hand",    "Presents an opposing perspective to balance or undermine the argument."),
    ("nevertheless",         "Asserts a counter-claim in spite of what was previously argued."),
    ("nonetheless",          "Pushes back against the conclusion despite acknowledging some merit."),
    ("despite",              "Introduces a fact that weakens the force of the supporting claim."),
    ("even so",              "Grants a concession but argues the conclusion still doesn't hold."),
    ("in contrast",          "Highlights a contradictory case that challenges the main point."),
    ("conversely",           "Reverses the logical direction of the argument being made."),
    ("that said",            "Qualifies the argument with a limiting counter-observation."),
    ("admittedly",           "Concedes a weakness in the argument before pivoting to a rebuttal."),
    ("granted",              "Temporarily accepts a premise only to show it doesn't support the conclusion."),
    ("this is false",        "Directly disputes the truth of the preceding claim."),
    ("this is wrong",        "Asserts that the argument or conclusion made is factually incorrect."),
    ("this misunderstands",  "Argues that the opposing view is based on a misreading or distortion."),
]

_REBUTTAL_MAP: Dict[str, str] = {m: e for m, e in REBUTTAL_MARKER_EXPLANATIONS}
_REBUTTAL_MARKERS_ORDERED = sorted(_REBUTTAL_MAP.keys(), key=len, reverse=True)

UNDERCUTTER_MARKERS = (
    "this does not mean", "this does not follow", "this is irrelevant",
    "this fails to account", "even if that were true", "the premise is flawed",
    "the assumption is false", "this is a false premise", "this assumes",
)

# ─── Rebuttal Generator Logic ───────────────────────────────────────────────

def generate_devils_advocate_rebuttals(premises: List[str]) -> List[str]:
    """Generates 3 strong counter-arguments to provided premises."""
    suggestions = []
    for i, p in enumerate(premises):
        if i >= 3: break  # Max 3 suggestions
        p_low = p.lower()
        if "because" in p_low or "since" in p_low:
            suggestions.append(f"An opponent might argue that the causal link in '{p[:40]}...' is speculative rather than proven.")
        elif any(w in p_low for w in ["research", "studies", "experts"]):
            suggestions.append(f"A critic could point out that the experts cited in '{p[:40]}...' might have a conflict of interest or biased sample.")
        else:
            suggestions.append(f"Wait, does '{p[:40]}...' actually follow? A counter-claim would be that this assumption is an oversimplification.")
    return list(set(suggestions))

# ─── Detect Counter-Arguments ───────────────────────────────────────────────

def _tokenise(text: str) -> Set[str]:
    return {w for w in re.findall(r'\b[a-z]{4,}\b', text.lower())}

def _overlap_ratio(a: Set[str], b: Set[str]) -> float:
    if not a or not b: return 0.0
    return len(a & b) / min(len(a), len(b))

def detect_counter_arguments(sentences: List[str], conclusion: Optional[str] = None, premises: Optional[List[str]] = None) -> List[Dict]:
    objections, seen_sentences = [], set()
    premise_tokens = [_tokenise(p) for p in (premises or [])]

    for s in sentences:
        s_clean, s_lower = s.strip(), s.strip().lower()
        if s_lower in seen_sentences: continue

        # Check Undercutters
        if any(m in s_lower for m in UNDERCUTTER_MARKERS):
            target_premise, best_ratio = None, 0.0
            s_tokens = _tokenise(s_clean)
            for i, pt in enumerate(premise_tokens):
                ratio = _overlap_ratio(s_tokens, pt)
                if ratio > best_ratio:
                    best_ratio, target_premise = ratio, (premises or [])[i]
            objections.append({
                "sentence": s_clean, "type": "undercutter", "target": target_premise or "a premise",
                "explanation": "Challenges the validity or truth of a supporting premise.",
                "confidence": round(min(0.9, 0.65 + best_ratio * 0.5), 2)
            }); seen_sentences.add(s_lower); continue

        # Check Rebuttals
        matched_marker = next((m for m in _REBUTTAL_MARKERS_ORDERED if s_lower.startswith(m)), None)
        if matched_marker:
            objections.append({
                "sentence": s_clean, "type": "rebuttal", "target": "conclusion",
                "explanation": _REBUTTAL_MAP[matched_marker], "confidence": 0.80
            }); seen_sentences.add(s_lower); continue

    return objections
