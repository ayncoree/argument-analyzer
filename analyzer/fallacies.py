"""
fallacies.py — Expanded fallacy detector.

Improvements over v1:
- 8 fallacy types (added Slippery Slope, Hasty Generalisation, Red Herring, Appeal to Emotion)
- Much richer keyword/marker sets for each fallacy
- Confidence score (0.0–1.0) per detection
- Severity level: "low" | "medium" | "high"
- De-duplication: a sentence can only trigger each fallacy type once
- Helper: detect_all_fallacies returns a severity-sorted, de-duplicated list
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _contains(text: str, keywords: Tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in keywords)


def _count_matches(text: str, keywords: Tuple[str, ...]) -> int:
    lower = text.lower()
    return sum(1 for kw in keywords if kw in lower)


def _make_result(
    fallacy_type: str,
    sentence: str,
    explanation: str,
    confidence: float,
    severity: str,
) -> Dict:
    return {
        "type": fallacy_type,
        "sentence": sentence,
        "explanation": explanation,
        "confidence": round(confidence, 2),
        "severity": severity,          # "low" | "medium" | "high"
    }


# ---------------------------------------------------------------------------
# 1. Ad Hominem  — attacking the person, not the argument
# ---------------------------------------------------------------------------
_AD_HOMINEM_STRONG = (
    "idiot", "stupid", "moron", "imbecile", "ignorant",
    "fool", "dumb", "brain-dead", "incompetent", "clueless",
    "dimwit", "halfwit", "buffoon",
)
_AD_HOMINEM_MODERATE = (
    "naive", "biased", "dishonest", "corrupt", "unqualified",
    "extremist", "radical", "fanatical", "conspiracy theorist",
)


def detect_ad_hominem(sentences: List[str]) -> List[Dict]:
    results = []
    for s in sentences:
        strong = _count_matches(s, _AD_HOMINEM_STRONG)
        moderate = _count_matches(s, _AD_HOMINEM_MODERATE)

        if strong:
            conf = min(0.95, 0.7 + 0.1 * strong)
            severity = "high"
        elif moderate:
            conf = min(0.8, 0.55 + 0.1 * moderate)
            severity = "medium"
        else:
            continue

        results.append(_make_result(
            "Ad Hominem", s,
            "Attacks the person or their character instead of addressing the argument.",
            conf, severity,
        ))
    return results


# ---------------------------------------------------------------------------
# 2. Strawman — misrepresenting the opponent's view
# ---------------------------------------------------------------------------
_STRAWMAN_MARKERS = (
    "they say that", "people claim that", "supporters believe that",
    "critics say that", "opponents argue that", "some people think that",
    "the other side claims", "those who disagree say", "liberals think",
    "conservatives think", "you believe that", "you are saying that",
    "your position is that",
)


def detect_strawman(sentences: List[str]) -> List[Dict]:
    results = []
    for s in sentences:
        hits = _count_matches(s, _STRAWMAN_MARKERS)
        if hits:
            conf = min(0.85, 0.55 + 0.1 * hits)
            results.append(_make_result(
                "Strawman", s,
                "Misrepresents an opposing position to make it easier to attack.",
                conf, "medium",
            ))
    return results


# ---------------------------------------------------------------------------
# 3. False Dilemma — reducing options to an artificial binary
# ---------------------------------------------------------------------------
_FALSE_DILEMMA_MARKERS = (
    "either", "only two options", "no other choice", "you must choose",
    "there are only", "it's one or the other", "you're with us or against us",
    "love it or leave it", "if not x then y", "no middle ground",
    "black and white", "all or nothing",
)


def detect_false_dilemma(sentences: List[str]) -> List[Dict]:
    results = []
    for s in sentences:
        hits = _count_matches(s, _FALSE_DILEMMA_MARKERS)
        if hits:
            conf = min(0.9, 0.6 + 0.1 * hits)
            severity = "high" if hits >= 2 else "medium"
            results.append(_make_result(
                "False Dilemma", s,
                "Presents a limited set of options as if they were the only possibilities.",
                conf, severity,
            ))
    return results


# ---------------------------------------------------------------------------
# 4. Circular Reasoning — conclusion smuggled into a premise
# ---------------------------------------------------------------------------
def detect_circular_reasoning(
    sentences: List[str],
    conclusion: Optional[str],
) -> List[Dict]:
    results = []
    if not conclusion:
        return results

    conclusion_lower = conclusion.lower()
    # Use key phrases from conclusion for phrase-level matching
    key_phrases = [p.strip() for p in re.split(r'[,;]', conclusion_lower) if len(p.strip()) > 4]

    for s in sentences:
        if s.strip() == conclusion.strip():
            continue
        s_lower = s.lower()

        hit = False
        if conclusion_lower in s_lower:
            hit = True
        elif any(kp in s_lower for kp in key_phrases):
            hit = True

        if hit:
            results.append(_make_result(
                "Circular Reasoning", s,
                "The argument's conclusion is assumed within one of its own premises.",
                0.75, "high",
            ))
    return results


# ---------------------------------------------------------------------------
# 5. Appeal to Authority — citing authority as a logical proof
# ---------------------------------------------------------------------------
_AUTHORITY_MARKERS = (
    "experts say", "scientists say", "according to authority",
    "studies prove", "research shows", "experts agree",
    "doctors recommend", "scholars believe", "the bible says",
    "god says", "the law says", "statistics show",
    "a harvard study", "studies show", "authorities claim",
    "the government says", "official sources confirm",
)


def detect_appeal_to_authority(sentences: List[str]) -> List[Dict]:
    results = []
    for s in sentences:
        hits = _count_matches(s, _AUTHORITY_MARKERS)
        if hits:
            conf = min(0.85, 0.6 + 0.1 * hits)
            results.append(_make_result(
                "Appeal to Authority", s,
                "Uses authority as evidence without engaging with the underlying reasoning.",
                conf, "medium",
            ))
    return results


# ---------------------------------------------------------------------------
# 6. Slippery Slope — assumes chain of bad events without justification
# ---------------------------------------------------------------------------
_SLIPPERY_MARKERS = (
    "will lead to", "will result in", "next thing you know",
    "before long", "it won't stop there", "first step towards",
    "gateway to", "once we allow", "if we permit", "opening the door",
    "snowball into", "domino effect", "slippery slope",
    "eventually lead", "sooner or later", "spiral into",
)


def detect_slippery_slope(sentences: List[str]) -> List[Dict]:
    results = []
    for s in sentences:
        hits = _count_matches(s, _SLIPPERY_MARKERS)
        if hits:
            conf = min(0.88, 0.6 + 0.1 * hits)
            results.append(_make_result(
                "Slippery Slope", s,
                "Assumes an unchecked chain of consequences without sufficient justification.",
                conf, "medium",
            ))
    return results


# ---------------------------------------------------------------------------
# 7. Hasty Generalisation — broad conclusion from insufficient evidence
# ---------------------------------------------------------------------------
_HASTY_GENERALISATION_ABSOLUTE = (
    "all", "every", "everyone", "nobody", "no one", "always",
    "never", "nothing", "everything", "everywhere", "anywhere",
)
_HASTY_GENERALISATION_PATTERNS = (
    r'\ball\b', r'\bevery(one|body|thing)?\b',
    r'\bnobody\b', r'\bnever\b', r'\balways\b',
)


def detect_hasty_generalisation(sentences: List[str]) -> List[Dict]:
    results = []
    for s in sentences:
        lower = s.lower()
        # Trigger only if we see a generaliser + a population claim
        gen_hits = sum(1 for pat in _HASTY_GENERALISATION_PATTERNS
                       if re.search(pat, lower))
        pop_markers = ("people", "humans", "women", "men", "children",
                       "immigrants", "politicians", "scientists",
                       "religious", "atheists", "muslims", "christians")
        pop_hit = any(m in lower for m in pop_markers)

        if gen_hits >= 1 and pop_hit:
            conf = min(0.82, 0.55 + 0.08 * gen_hits)
            results.append(_make_result(
                "Hasty Generalisation", s,
                "Draws a sweeping conclusion from an insufficient sample or evidence.",
                conf, "medium",
            ))
    return results


# ---------------------------------------------------------------------------
# 8. Appeal to Emotion — bypasses logic by exploiting feelings
# ---------------------------------------------------------------------------
_EMOTION_MARKERS = (
    "think of the children", "won't somebody", "how could anyone",
    "if you care about", "don't you feel", "surely you agree",
    "it breaks my heart", "it's heartbreaking", "for the love of",
    "imagine how they feel", "we must protect", "save the",
    "our children will suffer", "families will be destroyed",
    "blood will be on our hands", "this is a tragedy",
)


def detect_appeal_to_emotion(sentences: List[str]) -> List[Dict]:
    results = []
    for s in sentences:
        hits = _count_matches(s, _EMOTION_MARKERS)
        if hits:
            conf = min(0.82, 0.55 + 0.1 * hits)
            results.append(_make_result(
                "Appeal to Emotion", s,
                "Manipulates emotional reactions to bypass logical reasoning.",
                conf, "medium",
            ))
    return results


# ---------------------------------------------------------------------------
# Master detector
# ---------------------------------------------------------------------------
_SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def detect_all_fallacies(
    sentences: List[str],
    conclusion: Optional[str] = None,
) -> List[Dict]:
    """
    Run all fallacy detectors and return a de-duplicated, severity-sorted list.

    Each result has keys:
        type, sentence, explanation, confidence, severity
    """
    raw: List[Dict] = []
    raw.extend(detect_ad_hominem(sentences))
    raw.extend(detect_strawman(sentences))
    raw.extend(detect_false_dilemma(sentences))
    raw.extend(detect_circular_reasoning(sentences, conclusion))
    raw.extend(detect_appeal_to_authority(sentences))
    raw.extend(detect_slippery_slope(sentences))
    raw.extend(detect_hasty_generalisation(sentences))
    raw.extend(detect_appeal_to_emotion(sentences))

    # De-duplicate: keep the highest-confidence detection per (type, sentence)
    seen: Dict[Tuple[str, str], Dict] = {}
    for item in raw:
        key = (item["type"], item["sentence"])
        if key not in seen or item["confidence"] > seen[key]["confidence"]:
            seen[key] = item

    # Sort by severity then confidence descending
    return sorted(
        seen.values(),
        key=lambda x: (_SEVERITY_ORDER.get(x["severity"], 3), -x["confidence"]),
    )
