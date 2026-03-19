"""
ui/app.py — Argument Analyzer Pro (V3 — Top-Notch UI)
"""

import json
import datetime
import streamlit as st
import pandas as pd
import re

from analyzer.parser import split_sentences, extract_text_from_url, extract_text_from_pdf
from analyzer.classifier import (
    detect_conclusion_with_confidence,
    extract_premises,
    analyse_tone,
    compute_argument_strength,
)
from analyzer.fallacies import detect_all_fallacies
from analyzer.objections import detect_counter_arguments, generate_devils_advocate_rebuttals
import importlib
from analyzer import llm_deep_scan
importlib.reload(llm_deep_scan)
from analyzer.llm_deep_scan import run_ai_deep_scan, run_ai_compare, run_ai_constructor

st.set_page_config(
    page_title="Argument Analyzer Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# PREMIUM CSS — Animations, Glassmorphism, Neon Glows
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

/* ─── Global Reset ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background-color: #030712 !important;
    color: #e2e8f0 !important;
}
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { right: 10px !important; }

/* ─── Animated Background ──────────────────────────────────────────────────── */
.stApp {
    background: radial-gradient(ellipse at 20% 20%, rgba(59,130,246,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(6,182,212,0.04) 0%, transparent 70%),
                #030712 !important;
    background-attachment: fixed !important;
}

/* ─── Hero Section ─────────────────────────────────────────────────────────── */
@keyframes heroGlow {
    0%, 100% { box-shadow: 0 0 40px rgba(59,130,246,0.15), 0 0 80px rgba(139,92,246,0.08); }
    50%       { box-shadow: 0 0 60px rgba(59,130,246,0.25), 0 0 120px rgba(139,92,246,0.15); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseRing {
    0%   { transform: scale(1);    opacity: 1; }
    100% { transform: scale(1.4);  opacity: 0; }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes borderGlow {
    0%, 100% { border-color: rgba(59,130,246,0.3); }
    50%       { border-color: rgba(139,92,246,0.6); }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.5); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}

.hero {
    background: linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(17,24,39,0.95) 50%, rgba(15,23,42,0.95) 100%);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 24px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    animation: heroGlow 4s ease-in-out infinite, fadeSlideDown 0.6s ease-out;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4, #3b82f6);
    background-size: 200% 100%;
    animation: gradientShift 3s ease infinite;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #60a5fa;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 12px;
    animation: fadeSlideDown 0.4s ease-out;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 40%, #a78bfa 70%, #67e8f9 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 5s ease infinite, fadeSlideDown 0.5s ease-out;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.hero-sub {
    color: #475569;
    font-size: 1rem;
    margin-top: 8px;
    animation: fadeSlideDown 0.7s ease-out;
}
.hero-stats {
    display: flex;
    gap: 24px;
    margin-top: 20px;
    animation: fadeSlideUp 0.8s ease-out;
}
.hero-stat {
    text-align: center;
}
.hero-stat-num { font-size: 1.4rem; font-weight: 800; color: #60a5fa; }
.hero-stat-lbl { font-size: 0.68rem; color: #475569; text-transform: uppercase; letter-spacing: 0.05em; }

/* ─── Glass Cards ──────────────────────────────────────────────────────────── */
.glass-card {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 14px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    animation: fadeSlideUp 0.5s ease-out;
    position: relative;
    overflow: hidden;
}
.glass-card:hover {
    border-color: rgba(59,130,246,0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(59,130,246,0.12);
}
.glass-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(135deg, rgba(59,130,246,0.03) 0%, transparent 60%);
    pointer-events: none;
}

/* ─── Conclusion Card ──────────────────────────────────────────────────────── */
.conclusion-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(139,92,246,0.05) 100%);
    border: 1px solid rgba(59,130,246,0.25);
    border-left: 4px solid #3b82f6;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
    animation: slideInLeft 0.5s ease-out;
    transition: all 0.3s ease;
}
.conclusion-card:hover { box-shadow: 0 4px 24px rgba(59,130,246,0.2); }
.conclusion-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #3b82f6;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}
.conclusion-text {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f1f5f9;
    line-height: 1.5;
}

/* ─── Premise Cards ────────────────────────────────────────────────────────── */
.premise-card {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    transition: all 0.3s ease;
    animation: slideInLeft 0.5s ease-out;
}
.premise-card:hover {
    border-color: rgba(99,102,241,0.3);
    background: rgba(99,102,241,0.05);
    transform: translateX(4px);
}
.premise-num {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 800;
    color: white; flex-shrink: 0;
    box-shadow: 0 0 12px rgba(99,102,241,0.4);
}
.premise-text { font-size: 0.92rem; color: #cbd5e1; line-height: 1.5; padding-top: 4px; }

/* ─── Strength Gauge ───────────────────────────────────────────────────────── */
.gauge-wrap {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: float 3s ease-in-out infinite;
}
.gauge-ring {
    width: 120px; height: 120px;
    border-radius: 50%;
    margin: 0 auto 16px;
    position: relative;
    display: flex; align-items: center; justify-content: center;
}
.gauge-score {
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1;
    animation: countUp 0.6s cubic-bezier(0.34,1.56,0.64,1);
}
.gauge-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 6px;
}
.gauge-verdict {
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 8px;
}

/* ─── Fallacy Cards ────────────────────────────────────────────────────────── */
.fallacy-card {
    background: rgba(239,68,68,0.06);
    border: 1px solid rgba(239,68,68,0.2);
    border-left: 3px solid #ef4444;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    animation: slideInRight 0.5s ease-out;
    transition: all 0.3s ease;
}
.fallacy-card:hover { background: rgba(239,68,68,0.1); transform: translateX(-3px); }
.fallacy-type { font-size: 0.7rem; font-weight: 700; color: #ef4444; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.fallacy-text { font-size: 0.88rem; color: #fca5a5; line-height: 1.4; }

/* ─── Objection Cards ──────────────────────────────────────────────────────── */
.objection-card {
    background: rgba(245,158,11,0.06);
    border: 1px solid rgba(245,158,11,0.2);
    border-left: 3px solid #f59e0b;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    animation: slideInLeft 0.5s ease-out;
    transition: all 0.3s ease;
}
.objection-card:hover { background: rgba(245,158,11,0.1); transform: translateX(3px); }
.objection-type { font-size: 0.7rem; font-weight: 700; color: #f59e0b; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.objection-expl { font-size: 0.82rem; color: #64748b; margin-bottom: 6px; font-style: italic; }
.objection-text { font-size: 0.88rem; color: #fde68a; line-height: 1.4; }

/* ─── Devil's Advocate Cards ───────────────────────────────────────────────── */
.da-card {
    background: rgba(168,85,247,0.06);
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    animation: fadeSlideUp 0.5s ease-out;
    transition: all 0.3s ease;
    display: flex; gap: 12px; align-items: flex-start;
}
.da-card:hover { background: rgba(168,85,247,0.1); transform: scale(1.01); }
.da-icon { font-size: 1.4rem; flex-shrink: 0; }
.da-text { font-size: 0.9rem; color: #d8b4fe; line-height: 1.5; }

/* ─── AI Report Card ───────────────────────────────────────────────────────── */
.ai-report {
    background: linear-gradient(135deg, rgba(6,182,212,0.06) 0%, rgba(59,130,246,0.04) 100%);
    border: 1px solid rgba(6,182,212,0.2);
    border-top: 3px solid transparent;
    border-image: linear-gradient(90deg,#06b6d4,#3b82f6,#8b5cf6) 1;
    border-radius: 14px;
    padding: 22px;
    animation: fadeSlideUp 0.6s ease-out;
}
.ai-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px;
}
.ai-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #06b6d4;
    position: relative;
}
.ai-dot::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: #06b6d4;
    animation: pulseRing 1.5s ease-out infinite;
}

/* ─── Section Headers ──────────────────────────────────────────────────────── */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.section-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(139,92,246,0.2));
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    border: 1px solid rgba(59,130,246,0.2);
}
.section-title { font-size: 1rem; font-weight: 700; color: #f1f5f9; }

/* ─── Tone Meter ───────────────────────────────────────────────────────────── */
.tone-bar-wrap { margin: 10px 0; }
.tone-bar-label { display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b; margin-bottom: 6px; }
.tone-bar-bg { background: rgba(255,255,255,0.05); border-radius: 99px; height: 8px; overflow: hidden; }
.tone-bar-fill {
    height: 100%; border-radius: 99px;
    transition: width 1s cubic-bezier(0.4,0,0.2,1);
    animation: slideInLeft 0.8s ease-out;
}

/* ─── Metric Chips ─────────────────────────────────────────────────────────── */
.metrics-row { display: flex; gap: 12px; flex-wrap: wrap; margin: 16px 0; }
.metric-chip {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 12px 18px;
    flex: 1; min-width: 80px;
    text-align: center;
    transition: all 0.3s ease;
    animation: fadeSlideUp 0.5s ease-out;
}
.metric-chip:hover { border-color: rgba(59,130,246,0.3); transform: translateY(-2px); }
.metric-num { font-size: 1.4rem; font-weight: 800; color: #60a5fa; }
.metric-lbl { font-size: 0.68rem; color: #475569; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px; }

/* ─── Buttons ──────────────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    letter-spacing: 0.02em !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.4) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(59,130,246,0.5) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(15,23,42,0.8) !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    color: #a78bfa !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(139,92,246,0.1) !important;
    border-color: #8b5cf6 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(139,92,246,0.3) !important;
}

/* ─── Inputs ───────────────────────────────────────────────────────────────── */
textarea, .stTextInput > div > div > input {
    background: rgba(15,23,42,0.9) !important;
    border: 1px solid rgba(59,130,246,0.15) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    font-family: 'Inter', sans-serif !important;
}
textarea:focus, .stTextInput > div > div > input:focus {
    border-color: rgba(59,130,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
}

/* ─── Tabs ─────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    color: #475569 !important;
    transition: all 0.3s ease !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(59,130,246,0.08) !important;
    color: #60a5fa !important;
    border-bottom: 2px solid #3b82f6 !important;
}

/* ─── Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(10,15,28,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(20px) !important;
}

/* ─── Radio ────────────────────────────────────────────────────────────────── */
.stRadio > div { gap: 8px !important; }
.stRadio [data-testid="stMarkdownContainer"] p { font-size: 0.88rem !important; color: #94a3b8 !important; }
.stRadio [aria-checked="true"] + div p { color: #60a5fa !important; font-weight: 600 !important; }

/* ─── Progress / Confidence ────────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
    border-radius: 99px !important;
}

/* ─── Divider ──────────────────────────────────────────────────────────────── */
hr { border-color: rgba(255,255,255,0.05) !important; }

/* ─── Expander ─────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(15,23,42,0.5) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    transition: all 0.3s ease !important;
}
.streamlit-expanderHeader:hover {
    border-color: rgba(59,130,246,0.2) !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Session State Init
# ──────────────────────────────────────────────────────────────────────────────
if "history" not in st.session_state: st.session_state.history = []
if "results" not in st.session_state: st.session_state.results = {}
if "arg_input" not in st.session_state: st.session_state.arg_input = ""
if "analysis_done" not in st.session_state: st.session_state.analysis_done = False
if "ai_report" not in st.session_state: st.session_state.ai_report = ""
if "constructor_premises" not in st.session_state: st.session_state.constructor_premises = [""]

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def run_analysis_pipeline(text: str):
    sentences = split_sentences(text)
    conclusion, confidence, _ = detect_conclusion_with_confidence(sentences)
    premises = extract_premises(sentences, conclusion) if conclusion else []
    fallacies = detect_all_fallacies(sentences, conclusion)
    objections = detect_counter_arguments(sentences, conclusion, premises)
    devils_advocate = generate_devils_advocate_rebuttals(premises)
    tone = analyse_tone(sentences)
    score, str_label = compute_argument_strength(conclusion, premises, fallacies, objections)
    return {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "text": text, "sentences": sentences, "conclusion": conclusion,
        "confidence": confidence, "premises": premises, "fallacies": fallacies,
        "objections": objections, "devils_advocate": devils_advocate,
        "tone": tone, "score": score, "str_label": str_label
    }

def score_color(score: int) -> str:
    if score >= 75: return "#10b981"
    if score >= 50: return "#f59e0b"
    if score >= 25: return "#f97316"
    return "#ef4444"

def render_tone_bar(label: str, val: int, color: str):
    st.markdown(f"""
    <div class='tone-bar-wrap'>
        <div class='tone-bar-label'><span>{label}</span><span>{val}%</span></div>
        <div class='tone-bar-bg'><div class='tone-bar-fill' style='width:{val}%;background:{color};'></div></div>
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style='text-align:center;padding:10px 0 20px'>
        <div style='font-size:1.8rem'>🧠</div>
        <div style='font-weight:800;font-size:1.1rem;background:linear-gradient(90deg,#60a5fa,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>Analyzer Pro</div>
        <div style='font-size:0.7rem;color:#475569'>v3.0 — Gemini Powered</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**🔑 AI Core**")
    gemini_key = st.text_input("Gemini API Key", type="password", placeholder="Paste key from ai.google.dev", label_visibility="collapsed")
    if gemini_key:
        st.markdown("<div style='color:#10b981;font-size:0.75rem;margin-top:-8px'>✅ Key configured — AI features unlocked</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#475569;font-size:0.75rem;margin-top:-8px'>No key — AI features disabled</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**⚙️ Options**")
    show_raw = st.checkbox("Show Raw Source Text", value=False)

    st.markdown("---")
    st.markdown("**📜 Recent Analyses**")
    if st.session_state.history:
        for i, h in enumerate(reversed(st.session_state.history[-5:])):
            snip = (h.get("conclusion") or "No conclusion detected")[:30]
            score_c = score_color(h.get("score", 0))
            if st.button(f"↩ {snip}…", key=f"hist_{i}"):
                st.session_state.results = h
                st.session_state.analysis_done = True
                st.rerun()
    else:
        st.markdown("<div style='color:#334155;font-size:0.8rem;text-align:center;padding:10px'>No analyses yet</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.get("analysis_done"):
        export_data = {k: v for k, v in st.session_state.results.items() if k != "sentences"}
        st.download_button("📩 Export JSON", data=json.dumps(export_data, default=str), file_name="argument_analysis.json", use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# Hero
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-badge'>⚡ Powered by Gemini 2.5 Pro + Rule Engine</div>
    <div class='hero-title'>Argument Analyzer Pro</div>
    <div class='hero-sub'>Deconstruct fallacies, map logic, and stress-test arguments with AI.</div>
    <div class='hero-stats'>
        <div class='hero-stat'><div class='hero-stat-num'>18+</div><div class='hero-stat-lbl'>Discourse Markers</div></div>
        <div class='hero-stat'><div class='hero-stat-num'>8</div><div class='hero-stat-lbl'>Fallacy Types</div></div>
        <div class='hero-stat'><div class='hero-stat-num'>3</div><div class='hero-stat-lbl'>AI Modes</div></div>
        <div class='hero-stat'><div class='hero-stat-num'>∞</div><div class='hero-stat-lbl'>Languages*</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_analyze, tab_compare, tab_construct = st.tabs(["🔍  Analyze Source", "⚖️  Comparison Mode", "🧱  Constructor"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ANALYZE
# ══════════════════════════════════════════════════════════════════════════════
with tab_analyze:
    EXAMPLES = {
        "🌱 Climate": "Climate change is serious since emissions have risen 40% since 1990. Studies show temperatures are up 1.1°C. However, critics claim the models are wrong. Either we act now or civilisation collapses. Therefore, immediate action is necessary.",
        "💉 Vaccines": "Vaccines are safe and effective because they have undergone rigorous trials. Research shows vaccine-preventable diseases declined by 90%. However, some critics argue this without evidence. Widespread vaccination is the best public health strategy.",
        "📉 Economics": "Tax cuts stimulate the economy since they leave more money in people's hands. Experts say lower taxes correlate with higher GDP growth. But critics argue they disproportionately benefit the wealthy. Targeted reform is wiser than blanket cuts."
    }

    st.markdown("<div class='section-header'><div class='section-icon'>📥</div><div class='section-title'>Load Quick Example</div></div>", unsafe_allow_html=True)
    ec1, ec2, ec3 = st.columns(3)
    for col, (name, text) in zip([ec1, ec2, ec3], EXAMPLES.items()):
        if col.button(name, use_container_width=True):
            st.session_state["txt_input_main"] = text
            st.session_state["arg_input"] = text
            st.rerun()

    st.markdown("")
    src = st.radio("**Input Source**", ["✍️ Text", "🌐 Web URL", "📄 PDF File"], horizontal=True)
    source_text = ""

    if src == "✍️ Text":
        source_text = st.text_area("", value=st.session_state.arg_input, height=150,
                                   placeholder="Paste your argument here…", key="txt_input_main",
                                   label_visibility="collapsed")
    elif src == "🌐 Web URL":
        url = st.text_input("🌐 Web URL", placeholder="https://www.nature.com/articles/…")
        if url:
            with st.spinner("Scraping article text…"):
                source_text = extract_text_from_url(url)
                if not source_text: st.error("Could not fetch that URL.")
    elif src == "📄 PDF File":
        pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf:
            with st.spinner("Extracting PDF text…"):
                source_text = extract_text_from_pdf(pdf)

    st.markdown("")
    b1, b2 = st.columns(2)
    with b1:
        run_local = st.button("🚀 Analyze Logical Architecture", use_container_width=True, type="primary")
    with b2:
        run_ai = st.button("🤖 AI Deep Scan (Gemini)", use_container_width=True)

    if run_local:
        if source_text and len(source_text) > 5:
            with st.spinner("Deconstructing argument structure…"):
                results = run_analysis_pipeline(source_text)
                st.session_state.results = results
                st.session_state.analysis_done = True
                st.session_state.ai_report = ""
                st.session_state.history.append(results)
        else: st.warning("Please provide an argument first.")

    if run_ai:
        if not gemini_key: st.warning("Please enter your Gemini API Key in the sidebar.")
        elif source_text and len(source_text) > 5:
            with st.spinner("Gemini 2.5 Pro is performing deep logical deconstruction…"):
                results = run_analysis_pipeline(source_text)
                st.session_state.results = results
                st.session_state.analysis_done = True
                ai_report = run_ai_deep_scan(gemini_key, source_text)
                st.session_state.ai_report = ai_report
                st.session_state.history.append(results)
        else: st.warning("Please provide an argument first.")

    # ── Results ────────────────────────────────────────────────────────────────
    if st.session_state.get("analysis_done"):
        res = st.session_state.results
        st.markdown("---")

        # Metrics strip
        st.markdown(f"""
        <div class='metrics-row'>
            <div class='metric-chip'><div class='metric-num'>{res['score']}</div><div class='metric-lbl'>Logic Score</div></div>
            <div class='metric-chip'><div class='metric-num'>{len(res['premises'])}</div><div class='metric-lbl'>Premises</div></div>
            <div class='metric-chip'><div class='metric-num'>{len(res['fallacies'])}</div><div class='metric-lbl'>Fallacies</div></div>
            <div class='metric-chip'><div class='metric-num'>{len(res['objections'])}</div><div class='metric-lbl'>Counter-Args</div></div>
        </div>""", unsafe_allow_html=True)

        lc, rc = st.columns([2, 1])

        with lc:
            # Conclusion
            st.markdown("<div class='section-header'><div class='section-icon'>🎯</div><div class='section-title'>Identified Conclusion</div></div>", unsafe_allow_html=True)
            if res['conclusion']:
                st.markdown(f"""<div class='conclusion-card'>
                    <div class='conclusion-label'>Main Claim</div>
                    <div class='conclusion-text'>{res['conclusion']}</div>
                </div>""", unsafe_allow_html=True)
                st.progress(res['confidence'], f"Confidence: {int(res['confidence']*100)}%")
            else:
                st.markdown("<div class='glass-card' style='color:#64748b;text-align:center'>No explicit conclusion detected.</div>", unsafe_allow_html=True)

            # Premises
            st.markdown("<div class='section-header' style='margin-top:20px'><div class='section-icon'>📋</div><div class='section-title'>Supporting Premises</div></div>", unsafe_allow_html=True)
            if res['premises']:
                for i, p in enumerate(res['premises'], 1):
                    st.markdown(f"""<div class='premise-card'>
                        <div class='premise-num'>{i}</div>
                        <div class='premise-text'>{p}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("<div class='glass-card' style='color:#64748b;text-align:center;font-size:0.88rem'>No supporting premises extracted.</div>", unsafe_allow_html=True)

        with rc:
            # Strength gauge
            sc = score_color(res['score'])
            st.markdown(f"""<div class='gauge-wrap' style='border-color:{sc}22'>
                <div class='gauge-ring' style='border:6px solid {sc}22;box-shadow:0 0 30px {sc}44'>
                    <div>
                        <div class='gauge-score' style='color:{sc}'>{res['score']}</div>
                        <div style='font-size:0.62rem;color:#475569;text-transform:uppercase;letter-spacing:0.1em'>/ 100</div>
                    </div>
                </div>
                <div class='gauge-label'>Argument Strength</div>
                <div class='gauge-verdict' style='color:{sc}'>{res['str_label']}</div>
            </div>""", unsafe_allow_html=True)

            # Tone
            st.markdown("<div style='margin-top:16px'>", unsafe_allow_html=True)
            st.markdown("<div class='section-header'><div class='section-icon'>🎭</div><div class='section-title'>Tone Analysis</div></div>", unsafe_allow_html=True)
            tone = res['tone']
            st.markdown(f"<div style='text-align:center;font-size:1.1rem;font-weight:700;color:{tone['color']};margin-bottom:12px'>{tone['label']}</div>", unsafe_allow_html=True)
            render_tone_bar("Objective", tone['objective'], "#06b6d4")
            render_tone_bar("Aggressive", tone['aggressive'], "#ef4444")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Fallacies & Objections
        with st.expander("⚠️  Fallacies & Counter-Arguments", expanded=True):
            fc, oc = st.columns(2)
            with fc:
                st.markdown("<div class='section-header'><div class='section-icon'>🚫</div><div class='section-title'>Logical Fallacies</div></div>", unsafe_allow_html=True)
                if res['fallacies']:
                    for f in res['fallacies']:
                        sev = f.get('severity', '')
                        sev_badge = {"high":"🔴","medium":"🟡","low":"🟢"}.get(sev.lower() if sev else "", "⚪")
                        st.markdown(f"""<div class='fallacy-card'>
                            <div class='fallacy-type'>{sev_badge} {f['type']}</div>
                            <div class='fallacy-text'>{f['explanation']}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color:#10b981;font-size:0.9rem;padding:12px;text-align:center'>✅ No common fallacies detected</div>", unsafe_allow_html=True)
            with oc:
                st.markdown("<div class='section-header'><div class='section-icon'>↩️</div><div class='section-title'>Counter-Arguments</div></div>", unsafe_allow_html=True)
                if res['objections']:
                    for o in res['objections']:
                        st.markdown(f"""<div class='objection-card'>
                            <div class='objection-type'>{o['type'].upper()}</div>
                            <div class='objection-expl'>{o['explanation']}</div>
                            <div class='objection-text'>"{o['sentence']}"</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='color:#10b981;font-size:0.9rem;padding:12px;text-align:center'>✅ No explicit rebuttals found</div>", unsafe_allow_html=True)

        # Devil's Advocate
        with st.expander("😈  Challenge Mode — Devil's Advocate", expanded=False):
            st.markdown("<div style='color:#a78bfa;font-size:0.85rem;margin-bottom:16px;'>These AI-generated challenges help you pressure-test your logic before anyone else does.</div>", unsafe_allow_html=True)
            icons = ["💀", "🔪", "⚡"]
            for i, s in enumerate(res['devils_advocate'], 0):
                st.markdown(f"""<div class='da-card'>
                    <div class='da-icon'>{icons[i % len(icons)]}</div>
                    <div class='da-text'>{s}</div>
                </div>""", unsafe_allow_html=True)
            if not res['devils_advocate']:
                st.markdown("<div style='color:#475569;text-align:center;font-size:0.88rem'>No weaknesses generated — the argument may be strong.</div>", unsafe_allow_html=True)

        # AI Report
        if st.session_state.get("ai_report"):
            with st.expander("🤖  Gemini AI Deep Analysis Report", expanded=True):
                st.markdown(f"""<div class='ai-report'>
                    <div class='ai-header'>
                        <div class='ai-dot'></div>
                        <span style='font-size:0.75rem;font-weight:700;color:#06b6d4;letter-spacing:0.08em'>GEMINI AI FORMAL LOGIC DECONSTRUCTION</span>
                    </div>
                    {st.session_state.ai_report}
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab_compare:
    st.markdown("<div class='section-header'><div class='section-icon'>⚖️</div><div class='section-title'>Side-by-Side Logic Battle</div></div>", unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        st.markdown("<div style='font-weight:600;color:#60a5fa;margin-bottom:6px'>Argument A</div>", unsafe_allow_html=True)
        a_text = st.text_area("", height=150, key="comp_a", placeholder="Paste Argument A here…", label_visibility="collapsed")
    with cb:
        st.markdown("<div style='font-weight:600;color:#a78bfa;margin-bottom:6px'>Argument B</div>", unsafe_allow_html=True)
        b_text = st.text_area("", height=150, key="comp_b", placeholder="Paste Argument B here…", label_visibility="collapsed")

    cb1, cb2 = st.columns(2)
    with cb1: do_compare = st.button("🏁 Run Comparison Analysis", use_container_width=True, type="primary")
    with cb2: do_ai_judge = st.button("⚖️ AI Debate Judge (Gemini)", use_container_width=True)

    if do_compare and a_text and b_text:
        with st.spinner("Analyzing both arguments…"):
            ra, rb = run_analysis_pipeline(a_text), run_analysis_pipeline(b_text)

        sc_a, sc_b = score_color(ra['score']), score_color(rb['score'])
        st.markdown(f"""
        <div class='metrics-row' style='margin-top:20px'>
            <div class='metric-chip'><div class='metric-num' style='color:{sc_a}'>{ra['score']}</div><div class='metric-lbl'>A — Score</div></div>
            <div class='metric-chip'><div class='metric-num' style='color:{sc_b}'>{rb['score']}</div><div class='metric-lbl'>B — Score</div></div>
            <div class='metric-chip'><div class='metric-num'>{len(ra['premises'])}</div><div class='metric-lbl'>A — Premises</div></div>
            <div class='metric-chip'><div class='metric-num'>{len(rb['premises'])}</div><div class='metric-lbl'>B — Premises</div></div>
            <div class='metric-chip'><div class='metric-num'>{len(ra['fallacies'])}</div><div class='metric-lbl'>A — Fallacies</div></div>
            <div class='metric-chip'><div class='metric-num'>{len(rb['fallacies'])}</div><div class='metric-lbl'>B — Fallacies</div></div>
        </div>""", unsafe_allow_html=True)

        winner = "A 🏆" if ra['score'] > rb['score'] else ("B 🏆" if rb['score'] > ra['score'] else "Draw 🤝")
        st.markdown(f"<div style='text-align:center;padding:16px;background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.2);border-radius:14px;font-size:1.1rem;font-weight:700;color:#60a5fa;margin-top:12px'>Logical Winner: {winner}</div>", unsafe_allow_html=True)

    if do_ai_judge:
        if not gemini_key: st.warning("Please enter your Gemini API Key in the sidebar.")
        elif a_text and b_text:
            with st.spinner("The AI Judge is deliberating…"):
                ai_verdict = run_ai_compare(gemini_key, a_text, b_text)
            st.markdown(f"""<div class='ai-report' style='margin-top:16px'>
                <div class='ai-header'><div class='ai-dot'></div>
                    <span style='font-size:0.75rem;font-weight:700;color:#06b6d4;letter-spacing:0.08em'>AI DEBATE JUDGE — GEMINI VERDICT</span>
                </div>{ai_verdict}</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CONSTRUCTOR
# ══════════════════════════════════════════════════════════════════════════════
with tab_construct:
    st.markdown("<div class='section-header'><div class='section-icon'>🧱</div><div class='section-title'>Logic Chain Builder</div></div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#64748b;font-size:0.88rem;margin-bottom:20px'>Build your argument brick-by-brick. The AI Coach will check your logic chain and highlight any leaps of faith.</div>", unsafe_allow_html=True)

    for i in range(len(st.session_state.constructor_premises)):
        st.session_state.constructor_premises[i] = st.text_input(
            f"Premise {i+1}", value=st.session_state.constructor_premises[i], key=f"p_{i}",
            placeholder=f"Enter supporting premise {i+1}…"
        )

    pa, pb = st.columns(2)
    with pa: st.button("➕ Add Premise", on_click=lambda: st.session_state.constructor_premises.append(""), key="add_btn")
    with pb: st.button("➖ Remove", on_click=lambda: st.session_state.constructor_premises.pop() if len(st.session_state.constructor_premises) > 1 else None, key="rem_btn")

    st.markdown("<div style='margin:10px 0 4px;font-weight:600;color:#f1f5f9'>Conclusion</div>", unsafe_allow_html=True)
    c_input = st.text_input("", key="cons_claim", placeholder="Therefore… (enter your main claim here)", label_visibility="collapsed")

    va, vb = st.columns(2)
    with va: do_validate = st.button("🛠 Validate Logic Structure", use_container_width=True, type="primary")
    with vb: do_coach = st.button("🤖 AI Logic Coach (Gemini)", use_container_width=True)

    if do_validate:
        full = ". ".join(p for p in st.session_state.constructor_premises if p) + ". Therefore, " + c_input
        valid_res = run_analysis_pipeline(full)
        c_words = set(re.findall(r'\b[a-z]{4,}\b', c_input.lower()))
        p_words = set(re.findall(r'\b[a-z]{4,}\b', " ".join(st.session_state.constructor_premises).lower()))
        gaps = c_words - p_words

        sc = score_color(valid_res['score'])
        st.markdown(f"""<div class='glass-card' style='border-color:{sc}44;text-align:center;padding:24px'>
            <div style='font-size:2rem;font-weight:900;color:{sc}'>{valid_res['score']}</div>
            <div style='font-size:0.75rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-top:4px'>Logic Score — {valid_res['str_label']}</div>
        </div>""", unsafe_allow_html=True)

        if gaps and len(gaps) > 1:
            st.markdown(f"<div class='fallacy-card'><div class='fallacy-type'>⚠️ Leap of Faith Detected</div><div class='fallacy-text'>These terms appear in your conclusion but not in any premise: <strong>{', '.join(gaps)}</strong>. Your logic has a gap here.</div></div>", unsafe_allow_html=True)
        elif c_input:
            st.markdown("<div class='glass-card' style='border-color:#10b981;text-align:center;color:#10b981;font-weight:600'>🎯 No logic gaps detected — your argument flows correctly!</div>", unsafe_allow_html=True)
            st.balloons()

        if valid_res['fallacies']:
            st.markdown("<div class='fallacy-card' style='margin-top:8px'><div class='fallacy-type'>⚠️ Structural Errors</div>" + "".join(f"<div class='fallacy-text'>• {f['type']}: {f['explanation']}</div>" for f in valid_res['fallacies']) + "</div>", unsafe_allow_html=True)

    if do_coach:
        if not gemini_key: st.warning("Please enter your Gemini API Key in the sidebar.")
        else:
            full = ". ".join(p for p in st.session_state.constructor_premises if p) + ". Therefore, " + c_input
            with st.spinner("AI Logic Coach is reviewing your argument chain…"):
                ai_coach = run_ai_constructor(gemini_key, full)
            st.markdown(f"""<div class='ai-report' style='margin-top:16px'>
                <div class='ai-header'><div class='ai-dot'></div>
                    <span style='font-size:0.75rem;font-weight:700;color:#06b6d4;letter-spacing:0.08em'>AI LOGIC COACH — GEMINI FEEDBACK</span>
                </div>{ai_coach}</div>""", unsafe_allow_html=True)
