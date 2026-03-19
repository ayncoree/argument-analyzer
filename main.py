"""
main.py — CLI entry point for the Argument Analyzer.

Usage
-----
    python main.py "Your argument text here."
    python main.py  (interactive prompt)
    python main.py --help
"""

from __future__ import annotations

import argparse
import json
import sys

from analyzer.parser import split_sentences
from analyzer.classifier import (
    detect_conclusion_with_confidence,
    extract_premises,
    compute_argument_strength,
)
from analyzer.fallacies import detect_all_fallacies
from analyzer.objections import detect_counter_arguments


# ---------------------------------------------------------------------------
# ANSI colour helpers (degrade gracefully on Windows without colorama)
# ---------------------------------------------------------------------------
try:
    import colorama
    colorama.init(autoreset=True)
    _R = colorama.Fore.RED
    _G = colorama.Fore.GREEN
    _Y = colorama.Fore.YELLOW
    _B = colorama.Fore.CYAN
    _M = colorama.Fore.MAGENTA
    _W = colorama.Style.BRIGHT + colorama.Fore.WHITE
    _X = colorama.Style.RESET_ALL
except ImportError:
    _R = _G = _Y = _B = _M = _W = _X = ""


def _hr(char: str = "─", width: int = 60) -> str:
    return char * width


def _banner(text: str) -> None:
    print(f"\n{_W}{_hr()}")
    print(f"  {text}")
    print(f"{_hr()}{_X}")


def analyse(text: str, use_ml: bool = False, output_json: bool = False) -> None:
    sentences  = split_sentences(text)
    conclusion, confidence, _ = detect_conclusion_with_confidence(sentences, use_ml=use_ml)
    premises   = extract_premises(sentences, conclusion) if conclusion else []
    fallacies  = detect_all_fallacies(sentences, conclusion)
    objections = detect_counter_arguments(sentences, conclusion, premises)
    score, label = compute_argument_strength(conclusion, premises, fallacies, objections)

    if output_json:
        result = {
            "conclusion":     conclusion,
            "confidence":     round(confidence, 3),
            "premises":       premises,
            "strength_score": score,
            "strength_label": label,
            "fallacies": [
                {"type": f["type"], "sentence": f["sentence"],
                 "severity": f["severity"], "confidence": f["confidence"]}
                for f in fallacies
            ],
            "counter_arguments": [
                {"type": o["type"], "sentence": o["sentence"],
                 "explanation": o["explanation"]}
                for o in objections
            ],
        }
        print(json.dumps(result, indent=2))
        return

    # Human-readable output
    _banner("🧠 ARGUMENT ANALYZER — RESULTS")

    print(f"\n{_B}══ CONCLUSION {'(' + str(int(confidence*100)) + '% confidence)':>30} ══{_X}")
    if conclusion:
        print(f"  {_W}{conclusion}{_X}")
    else:
        print(f"  {_Y}No clear conclusion detected.{_X}")

    print(f"\n{_G}══ PREMISES ══{_X}")
    if premises:
        for i, p in enumerate(premises, 1):
            print(f"  {i}. {p}")
    else:
        print(f"  {_Y}None detected.{_X}")

    print(f"\n{_R}══ LOGICAL FALLACIES ══{_X}")
    if fallacies:
        for f in fallacies:
            sev = f["severity"].upper()
            print(f"  [{sev}] {_M}{f['type']}{_X} — {f['explanation']}")
            print(f"       \"{f['sentence'][:80]}{'…' if len(f['sentence'])>80 else ''}\"")
    else:
        print(f"  {_G}✅ No fallacies detected.{_X}")

    print(f"\n{_Y}══ COUNTER-ARGUMENTS ══{_X}")
    if objections:
        for o in objections:
            print(f"  [{o['type'].upper()}] {o['sentence'][:80]}{'…' if len(o['sentence'])>80 else ''}")
            print(f"       → {o['explanation']}")
    else:
        print(f"  {_G}✅ No counter-arguments detected.{_X}")

    print(f"\n{_B}══ ARGUMENT STRENGTH ══{_X}")
    strength_color = _G if score >= 75 else (_B if score >= 50 else (_Y if score >= 25 else _R))
    bar = "█" * (score // 10) + "░" * (10 - score // 10)
    print(f"  {strength_color}{bar}  {score}/100 — {label}{_X}")

    print(f"\n{_hr()}\n")


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="argument-analyzer",
        description="Analyse the logical structure of a natural-language argument.",
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Argument text to analyse (or omit for interactive mode).",
    )
    parser.add_argument(
        "--ml",
        action="store_true",
        help="Enable ML-assisted clause classification.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output results as JSON.",
    )

    args = parser.parse_args()

    if args.text:
        analyse(args.text, use_ml=args.ml, output_json=args.output_json)
    else:
        print(f"{_W}Argument Analyzer — Interactive Mode{_X}")
        print("Type your argument (or 'quit' to exit):\n")
        while True:
            try:
                text = input(">>> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                sys.exit(0)

            if text.lower() in {"quit", "exit", "q"}:
                print("Goodbye.")
                break

            if text:
                analyse(text, use_ml=args.ml, output_json=args.output_json)


if __name__ == "__main__":
    main()
