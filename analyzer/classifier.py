"""
classifier.py — Upgraded Next-Gen Classifier with Sentiment & Tone Analysis

Features:
- Causal connective splitting
- Conclusion + Premise detection (Confidence-based)
- Argument Strength Heuristic
- NEW: Sentiment & Tone Analysis (Objective vs. Aggressive)
"""

from __future__ import annotations
import re
from typing import Dict, List, Optional, Tuple

try:
    from analyzer.ml_classifier import ml_classify_clause
    ML_AVAILABLE = True
except Exception:
    ML_AVAILABLE = False

# ──────────────────────────────────────────────────────────────────────────────
# Tone Analysis Constants
# ──────────────────────────────────────────────────────────────────────────────

AGGRESSIVE_MARKERS = {
    "ridiculous", "absurd", "nonsense", "blatantly", "obviously", "stupid",
    "clearly wrong", "dangerous", "threat", "insulting", "pathetic",
    "must accept", "stop lying", "liars", "failure", "clueless",
}

OBJECTIVE_MARKERS = {
    "evidence suggests", "research indicates", "it is possible",
    "some experts", "alternatively", "conflicting data", "study shows",
    "in light of", "consistent with", "preliminary", "appears that",
}

# ──────────────────────────────────────────────────────────────────────────────
# Existing Conclusion/Premise Logic (Optimised)
# ──────────────────────────────────────────────────────────────────────────────

EXPLICIT_CONCLUSION_MARKERS = [
    "therefore", "thus", "hence", "it follows that", "in conclusion",
    "we can conclude", "this shows that", "this proves that", "the result is",
    "accordingly", "consequently", "we may infer", "this means that",
    "so we can see", "this demonstrates",
    "por lo tanto", "entonces", "en conclusión", "concluimos que",  # Spanish
    "donc", "ainsi", "en conclusion", "il s'ensuit que"            # French
]

CAUSAL_CONNECTIVES = [
    " because ", " since ", " as ", " due to ", " given that ",
    " for the reason that ", " on account of ", " in light of ",
    " porque ", " ya que ", " dado que ", " pues ",                # Spanish
    " parce que ", " car ", " puisque ", " étant donné que "        # French
]

OBJECTION_STARTERS = [
    "however", "but", "although", "yet", "on the other hand",
    "nevertheless", "nonetheless", "despite", "even so",
]

SUPPORT_MARKERS = [
    "because", "since", "as", "given that", "the reason is",
    "the evidence shows", "data show", "studies indicate",
]

def split_compound(sentence: str) -> Tuple[str, Optional[str]]:
    lowered = sentence.lower()
    for connective in CAUSAL_CONNECTIVES:
        if connective in lowered:
            idx = lowered.index(connective)
            head = sentence[:idx].strip()
            tail = sentence[idx + len(connective):].strip()
            if head and tail: return head, tail
    return sentence.strip(), None

def detect_conclusion_with_confidence(sentences: List[str], use_ml: bool = False) -> Tuple[Optional[str], float, List[str]]:
    def _is_assertive(s: str) -> bool:
        sl = s.lower().strip()
        return not s.strip().endswith("?") and not any(sl.startswith(m) for m in OBJECTION_STARTERS)

    for s in sentences:
        s_lower = s.lower()
        if any(m in s_lower for m in EXPLICIT_CONCLUSION_MARKERS):
            return s.strip(), 0.95, []

    for s in reversed(sentences):
        if _is_assertive(s):
            head, _ = split_compound(s)
            return head.strip(), 0.65, []

    if use_ml and ML_AVAILABLE:
        for s in sentences:
            try:
                label, conf = ml_classify_clause(s)
                if label == "conclusion" and conf > 0.6:
                    return s.strip(), conf, []
            except Exception: pass

    return None, 0.0, []

def extract_premises(sentences: List[str], conclusion: Optional[str]) -> List[str]:
    seen, premises = set(), []
    def _add(p: str):
        p = p.strip()
        if p and p.lower() not in seen:
            seen.add(p.lower()); premises.append(p)

    conclusion_lower = conclusion.lower() if conclusion else ""
    for s in sentences:
        head, tail = split_compound(s)
        if tail:
            _add(tail)
            if head.lower() != conclusion_lower: _add(head)
            continue
        s_lower = s.lower()
        if any(f" {m} " in f" {s_lower} " for m in SUPPORT_MARKERS):
            _add(s); continue
        if conclusion_lower and s.lower().strip() == conclusion_lower: continue
        if not s.strip().endswith("?"): _add(s)
    return premises

def compute_argument_strength(conclusion: Optional[str], premises: List[str], fallacies: List[Dict], objections: List[Dict]) -> Tuple[int, str]:
    score = 50 + (10 if conclusion else 0) + min(30, len(premises) * 10)
    score -= min(40, len(fallacies) * 8) + min(20, len(objections) * 5)
    score = max(0, min(100, score))
    labels = {75: "Strong", 50: "Moderate", 25: "Weak", 0: "Very Weak"}
    label = next(l for k, l in sorted(labels.items(), reverse=True) if score >= k)
    return int(score), label

# ─── New Tone Analysis Logic ──────────────────────────────────────────────

def analyse_tone(sentences: List[str]) -> Dict:
    """Classify the overall tone of an argument into Tone Scores."""
    text = " ".join(sentences).lower()
    agg_count = sum(1 for m in AGGRESSIVE_MARKERS if m in text)
    obj_count = sum(1 for m in OBJECTIVE_MARKERS if m in text)

    # Simple normalization into 0-100 scores
    agg_score = min(100, agg_count * 25)
    obj_score = min(100, obj_count * 20)

    # Determine dominant tone label
    if agg_score > obj_score + 10:
        label = "Aggressive 😤"
        color = "#ff4b4b"
    elif obj_score > agg_score + 10:
        label = "Objective ⚖️"
        color = "#00d4ff"
    else:
        label = "Balanced 🤝"
        color = "#ffffff"

    return {
        "aggressive": agg_score,
        "objective": obj_score,
        "label": label,
        "color": color
    }
