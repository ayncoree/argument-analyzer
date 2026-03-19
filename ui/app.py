"""
ui/app.py — Argument Analyzer Pro (V3 — Top-Notch UI)
"""

import json
import datetime
import streamlit as st
import pandas as pd
import re

import importlib
from analyzer import parser, llm_deep_scan
importlib.reload(parser)
importlib.reload(llm_deep_scan)

from analyzer.parser import split_sentences, extract_text_from_url, extract_text_from_pdf, extract_text_from_youtube
from analyzer.llm_deep_scan import (
    run_ai_deep_scan, run_ai_compare, run_ai_constructor,
    run_ai_fact_check, run_ai_debate_response, run_ai_dejargonize, transcribe_audio_with_gemini,
    run_ai_full_pipeline
)


st.set_page_config(
    page_title="Argument Analyzer Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# LIQUID GLASS V2 — Ultra-Premium Flowing Refractive Design System
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background-color: #010816 !important;
    color: #e2e8f0 !important;
}
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { right: 10px !important; }

/* ═══ LIQUID WAVE BACKGROUND ═══ */
@keyframes auroraFlow {
    0%   { background-position: 0% 0%, 100% 100%, 50% 50%, 0% 100%; }
    25%  { background-position: 50% 100%, 0% 0%, 100% 50%, 100% 0%; }
    50%  { background-position: 100% 50%, 50% 50%, 0% 100%, 50% 50%; }
    75%  { background-position: 50% 0%, 100% 100%, 50% 0%, 0% 100%; }
    100% { background-position: 0% 0%, 100% 100%, 50% 50%, 0% 100%; }
}
@keyframes orbFloat1 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(60px, -40px) scale(1.1); }
    50% { transform: translate(-30px, 60px) scale(0.9); }
    75% { transform: translate(40px, 30px) scale(1.05); }
}
@keyframes orbFloat2 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(-50px, 50px) scale(1.15); }
    66% { transform: translate(70px, -30px) scale(0.85); }
}
@keyframes orbFloat3 {
    0%, 100% { transform: translate(0, 0) scale(1); }
    20% { transform: translate(40px, 40px) scale(1.1); }
    60% { transform: translate(-60px, -20px) scale(0.95); }
    80% { transform: translate(20px, -50px) scale(1.05); }
}
.stApp {
    background:
        radial-gradient(ellipse 700px 500px at 15% 25%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 600px 600px at 80% 75%, rgba(139,92,246,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 500px 400px at 50% 50%, rgba(6,182,212,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 800px 300px at 60% 10%, rgba(236,72,153,0.1) 0%, transparent 60%),
        #010816 !important;
    background-attachment: fixed !important;
    animation: auroraFlow 25s ease-in-out infinite !important;
}
/* Floating light orbs behind glass */
.stApp::before {
    content: '';
    position: fixed;
    top: 10%; left: 8%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
    border-radius: 50%;
    filter: blur(60px);
    animation: orbFloat1 18s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: 15%; right: 10%;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(6,182,212,0.18) 0%, transparent 70%);
    border-radius: 50%;
    filter: blur(50px);
    animation: orbFloat2 22s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

/* ═══ ADVANCED KEYFRAMES ═══ */
@keyframes glassRefract {
    0%, 100% { border-color: rgba(99,102,241,0.12); box-shadow: 0 8px 32px rgba(6,182,212,0.04), inset 0 1px 0 rgba(255,255,255,0.03); }
    33%      { border-color: rgba(6,182,212,0.2);   box-shadow: 0 12px 48px rgba(139,92,246,0.06), inset 0 1px 0 rgba(255,255,255,0.05); }
    66%      { border-color: rgba(236,72,153,0.15);  box-shadow: 0 8px 40px rgba(99,102,241,0.05), inset 0 1px 0 rgba(255,255,255,0.04); }
}
@keyframes waveFloat {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25%      { transform: translateY(-4px) rotate(0.3deg); }
    50%      { transform: translateY(-7px) rotate(-0.2deg); }
    75%      { transform: translateY(-3px) rotate(0.1deg); }
}
@keyframes liquidMorph {
    0%, 100% { border-radius: 28px; }
    25%      { border-radius: 30px 26px 32px 24px; }
    50%      { border-radius: 24px 32px 26px 30px; }
    75%      { border-radius: 32px 24px 28px 28px; }
}
@keyframes flowIn {
    from { opacity: 0; transform: translateY(28px) scale(0.96); filter: blur(6px); }
    to   { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}
@keyframes flowLeft {
    from { opacity: 0; transform: translateX(-24px) scale(0.98); filter: blur(4px); }
    to   { opacity: 1; transform: translateX(0) scale(1); filter: blur(0); }
}
@keyframes flowRight {
    from { opacity: 0; transform: translateX(24px) scale(0.98); filter: blur(4px); }
    to   { opacity: 1; transform: translateX(0) scale(1); filter: blur(0); }
}
@keyframes iridescent {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes auroraShimmer {
    0%   { opacity: 0.3; transform: translateX(-100%) skewX(-15deg); }
    50%  { opacity: 0.6; }
    100% { opacity: 0.3; transform: translateX(200%) skewX(-15deg); }
}
@keyframes pulseGlow {
    0%   { transform: scale(1);   opacity: 1; }
    100% { transform: scale(2); opacity: 0; }
}
@keyframes countPop {
    from { opacity: 0; transform: scale(0.2); filter: blur(12px); }
    to   { opacity: 1; transform: scale(1); filter: blur(0); }
}
@keyframes borderStream {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

.hero {
    background: linear-gradient(160deg, rgba(8,12,28,0.4) 0%, rgba(12,16,36,0.35) 50%, rgba(8,12,28,0.4) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 48px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    animation: flowIn 0.8s cubic-bezier(0.22,1,0.36,1), glassRefract 8s ease-in-out infinite, liquidMorph 12s ease-in-out infinite, waveFloat 8s ease-in-out infinite;
    backdrop-filter: blur(50px) saturate(1.6);
    -webkit-backdrop-filter: blur(50px) saturate(1.6);
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6366f1, #06b6d4, #ec4899, #8b5cf6, transparent);
    background-size: 300% 100%;
    animation: borderStream 3s linear infinite;
}
.hero::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.02), rgba(99,102,241,0.03), transparent);
    animation: auroraShimmer 6s ease-in-out infinite;
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center; gap: 7px;
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 99px;
    padding: 6px 16px;
    font-size: 0.68rem; font-weight: 700;
    color: #818cf8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 16px;
    backdrop-filter: blur(12px);
    animation: flowIn 0.5s ease-out;
    position: relative;
    z-index: 1;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    background: linear-gradient(135deg, #ffffff 0%, #93c5fd 20%, #c4b5fd 40%, #67e8f9 60%, #f0abfc 80%, #ffffff 100%);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: iridescent 8s ease infinite, flowIn 0.6s ease-out;
    line-height: 1.02;
    letter-spacing: -0.04em;
    position: relative;
    z-index: 1;
}
.hero-sub {
    color: #64748b; font-size: 1.05rem;
    margin-top: 12px;
    animation: flowIn 0.9s ease-out;
    position: relative; z-index: 1;
    letter-spacing: 0.01em;
}
.hero-stats {
    display: flex; gap: 32px;
    margin-top: 24px;
    animation: flowIn 1.1s ease-out;
    position: relative; z-index: 1;
}
.hero-stat {
    text-align: center;
    transition: transform 0.4s cubic-bezier(0.22,1,0.36,1);
}
.hero-stat:hover { transform: translateY(-3px) scale(1.05); }
.hero-stat-num {
    font-size: 1.6rem; font-weight: 800; color: #818cf8;
    font-family: 'Space Grotesk', sans-serif;
    text-shadow: 0 0 24px rgba(129,140,248,0.3);
}
.hero-stat-lbl { font-size: 0.62rem; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; }

/* ═══ LIQUID GLASS CARD ═══ */
.glass-card {
    background: linear-gradient(145deg, rgba(12,17,35,0.35) 0%, rgba(16,22,44,0.25) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 24px 26px;
    margin-bottom: 14px;
    backdrop-filter: blur(40px) saturate(1.5);
    -webkit-backdrop-filter: blur(40px) saturate(1.5);
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1);
    animation: flowIn 0.5s ease-out, glassRefract 10s ease-in-out infinite;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.015), rgba(99,102,241,0.02), transparent);
    animation: auroraShimmer 8s ease-in-out infinite;
    pointer-events: none;
}
.glass-card:hover {
    border-color: rgba(99,102,241,0.2);
    transform: translateY(-4px) scale(1.005);
    box-shadow: 0 16px 48px rgba(99,102,241,0.08), 0 0 80px rgba(6,182,212,0.03), inset 0 1px 0 rgba(255,255,255,0.04);
}

/* ═══ LIQUID CONCLUSION CARD ═══ */
.conclusion-card {
    background: linear-gradient(150deg, rgba(59,130,246,0.1) 0%, rgba(139,92,246,0.07) 40%, rgba(6,182,212,0.05) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid;
    border-image: linear-gradient(180deg, #6366f1, #06b6d4, #ec4899) 1;
    border-radius: 18px;
    padding: 24px 26px;
    margin-bottom: 14px;
    animation: flowLeft 0.6s ease-out, glassRefract 10s ease-in-out infinite;
    backdrop-filter: blur(36px) saturate(1.4);
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    overflow: hidden;
}
.conclusion-card::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.02), rgba(99,102,241,0.03), transparent);
    animation: auroraShimmer 7s ease-in-out infinite;
    pointer-events: none;
}
.conclusion-card:hover {
    box-shadow: 0 12px 40px rgba(99,102,241,0.12), 0 0 80px rgba(6,182,212,0.04);
    transform: translateX(4px) scale(1.005);
}
.conclusion-label {
    font-size: 0.62rem; font-weight: 800;
    color: #818cf8;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 10px;
    text-shadow: 0 0 16px rgba(129,140,248,0.2);
}
.conclusion-text {
    font-size: 1.14rem; font-weight: 600;
    color: #f1f5f9; line-height: 1.6;
    font-family: 'Space Grotesk', 'Inter', sans-serif;
}

/* ═══ LIQUID PREMISE CARDS ═══ */
.premise-card {
    background: linear-gradient(140deg, rgba(12,17,35,0.3) 0%, rgba(16,22,44,0.2) 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1);
    animation: flowLeft 0.5s ease-out;
    backdrop-filter: blur(30px) saturate(1.3);
    position: relative;
    overflow: hidden;
}
.premise-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.02), transparent);
    pointer-events: none;
    transition: left 0.6s ease;
}
.premise-card:hover::before { left: 150%; }
.premise-card:hover {
    border-color: rgba(99,102,241,0.18);
    background: linear-gradient(140deg, rgba(99,102,241,0.06) 0%, rgba(6,182,212,0.03) 100%);
    transform: translateX(6px) scale(1.008);
    box-shadow: 0 6px 28px rgba(99,102,241,0.06);
}
.premise-num {
    width: 32px; height: 32px;
    background: linear-gradient(145deg, #6366f1, #818cf8, #a78bfa);
    background-size: 200% 200%;
    animation: iridescent 4s ease infinite;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; font-weight: 800;
    color: white; flex-shrink: 0;
    box-shadow: 0 0 20px rgba(99,102,241,0.25);
    transition: all 0.4s cubic-bezier(0.22,1,0.36,1);
}
.premise-card:hover .premise-num {
    box-shadow: 0 0 32px rgba(99,102,241,0.5);
    transform: scale(1.1) rotate(3deg);
}
.premise-text { font-size: 0.92rem; color: #cbd5e1; line-height: 1.6; padding-top: 5px; }

/* ═══ LIQUID GAUGE ═══ */
.gauge-wrap {
    background: linear-gradient(160deg, rgba(12,17,35,0.35) 0%, rgba(16,22,44,0.25) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: waveFloat 6s ease-in-out infinite, glassRefract 10s ease-in-out infinite;
    backdrop-filter: blur(44px) saturate(1.5);
}
.gauge-wrap::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(99,102,241,0.04) 0%, transparent 45%);
    pointer-events: none;
    animation: auroraFlow 15s ease-in-out infinite;
}
.gauge-wrap::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.01), transparent);
    animation: auroraShimmer 9s ease-in-out infinite;
    pointer-events: none;
}
.gauge-ring {
    width: 140px; height: 140px;
    border-radius: 50%;
    margin: 0 auto 20px;
    position: relative;
    display: flex; align-items: center; justify-content: center;
}
.gauge-score {
    font-size: 3.2rem;
    font-weight: 900;
    font-family: 'Space Grotesk', sans-serif;
    line-height: 1;
    animation: countPop 0.8s cubic-bezier(0.34,1.56,0.64,1);
    text-shadow: 0 0 50px currentColor;
}
.gauge-label {
    font-size: 0.75rem; font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 8px;
}
.gauge-verdict {
    font-size: 1.12rem; font-weight: 700;
    margin-top: 10px;
    text-shadow: 0 0 24px currentColor;
    font-family: 'Space Grotesk', sans-serif;
}

/* ═══ LIQUID FALLACY CARDS ═══ */
.fallacy-card {
    background: linear-gradient(140deg, rgba(239,68,68,0.05) 0%, rgba(220,38,38,0.02) 100%);
    border: 1px solid rgba(239,68,68,0.12);
    border-left: 3px solid;
    border-image: linear-gradient(180deg, #ef4444, #f97316, #ec4899) 1;
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 10px;
    animation: flowRight 0.5s ease-out;
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1);
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}
.fallacy-card::before {
    content: '';
    position: absolute;
    top: 0; right: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(239,68,68,0.02), transparent);
    pointer-events: none;
    transition: right 0.6s ease;
}
.fallacy-card:hover::before { right: -50%; }
.fallacy-card:hover {
    background: linear-gradient(140deg, rgba(239,68,68,0.08) 0%, rgba(220,38,38,0.04) 100%);
    transform: translateX(-5px) scale(1.005);
    box-shadow: 0 6px 28px rgba(239,68,68,0.08);
}
.fallacy-type { font-size: 0.65rem; font-weight: 800; color: #ef4444; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 5px; text-shadow: 0 0 12px rgba(239,68,68,0.2); }
.fallacy-text { font-size: 0.88rem; color: #fca5a5; line-height: 1.5; }

/* ═══ LIQUID OBJECTION CARDS ═══ */
.objection-card {
    background: linear-gradient(140deg, rgba(245,158,11,0.05) 0%, rgba(217,119,6,0.02) 100%);
    border: 1px solid rgba(245,158,11,0.12);
    border-left: 3px solid;
    border-image: linear-gradient(180deg, #f59e0b, #eab308, #84cc16) 1;
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 10px;
    animation: flowLeft 0.5s ease-out;
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1);
    backdrop-filter: blur(12px);
}
.objection-card:hover {
    background: linear-gradient(140deg, rgba(245,158,11,0.08) 0%, rgba(217,119,6,0.04) 100%);
    transform: translateX(5px) scale(1.005);
    box-shadow: 0 6px 28px rgba(245,158,11,0.06);
}
.objection-type { font-size: 0.65rem; font-weight: 800; color: #f59e0b; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 5px; text-shadow: 0 0 12px rgba(245,158,11,0.2); }
.objection-expl { font-size: 0.82rem; color: #94a3b8; margin-bottom: 6px; font-style: italic; }
.objection-text { font-size: 0.88rem; color: #fde68a; line-height: 1.5; }

/* ═══ LIQUID DA CARDS ═══ */
.da-card {
    background: linear-gradient(140deg, rgba(168,85,247,0.05) 0%, rgba(139,92,246,0.02) 100%);
    border: 1px solid rgba(168,85,247,0.12);
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 10px;
    animation: flowIn 0.5s ease-out;
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1);
    display: flex; gap: 14px; align-items: flex-start;
    backdrop-filter: blur(12px);
}
.da-card:hover {
    background: linear-gradient(140deg, rgba(168,85,247,0.08) 0%, rgba(139,92,246,0.04) 100%);
    transform: scale(1.012) translateY(-3px);
    box-shadow: 0 10px 36px rgba(168,85,247,0.08);
}
.da-icon { font-size: 1.4rem; flex-shrink: 0; filter: drop-shadow(0 0 10px rgba(168,85,247,0.4)); }
.da-text { font-size: 0.9rem; color: #d8b4fe; line-height: 1.55; }

/* ═══ LIQUID AI REPORT ═══ */
.ai-report {
    background: linear-gradient(150deg, rgba(6,182,212,0.06) 0%, rgba(59,130,246,0.03) 40%, rgba(139,92,246,0.03) 100%);
    border: 1px solid rgba(6,182,212,0.12);
    border-top: 2px solid transparent;
    border-image: linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6, #ec4899, #06b6d4) 1;
    border-radius: 20px;
    padding: 26px;
    animation: flowIn 0.7s ease-out, glassRefract 10s ease-in-out infinite;
    backdrop-filter: blur(20px) saturate(1.2);
    position: relative;
    overflow: hidden;
}
.ai-report::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(6,182,212,0.02), transparent);
    animation: auroraShimmer 7s ease-in-out infinite;
    pointer-events: none;
}
.ai-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 18px;
}
.ai-dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: linear-gradient(135deg, #06b6d4, #22d3ee);
    position: relative;
    box-shadow: 0 0 16px rgba(6,182,212,0.6);
}
.ai-dot::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: #06b6d4;
    animation: pulseGlow 2s ease-out infinite;
}

/* ═══ LIQUID SECTION HEADERS ═══ */
.section-header {
    display: flex; align-items: center; gap: 13px;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(148,163,184,0.05);
}
.section-icon {
    width: 38px; height: 38px;
    background: linear-gradient(150deg, rgba(99,102,241,0.12), rgba(6,182,212,0.08));
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    border: 1px solid rgba(99,102,241,0.1);
    box-shadow: 0 0 20px rgba(99,102,241,0.06);
    transition: all 0.4s cubic-bezier(0.22,1,0.36,1);
}
.section-header:hover .section-icon {
    box-shadow: 0 0 28px rgba(99,102,241,0.12);
    transform: scale(1.08) rotate(2deg);
}
.section-title { font-size: 1.02rem; font-weight: 700; color: #f1f5f9; letter-spacing: -0.01em; font-family: 'Space Grotesk', 'Inter', sans-serif; }

/* ═══ LIQUID TONE METER ═══ */
.tone-bar-wrap { margin: 14px 0; }
.tone-bar-label { display: flex; justify-content: space-between; font-size: 0.74rem; color: #64748b; margin-bottom: 8px; }
.tone-bar-bg {
    background: rgba(148,163,184,0.05);
    border-radius: 99px;
    height: 9px;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,0.03);
}
.tone-bar-fill {
    height: 100%; border-radius: 99px;
    transition: width 1.4s cubic-bezier(0.22,1,0.36,1);
    animation: flowLeft 1s ease-out;
    box-shadow: 0 0 14px currentColor;
}

/* ═══ LIQUID METRIC CHIPS ═══ */
.metrics-row { display: flex; gap: 14px; flex-wrap: wrap; margin: 20px 0; }
.metric-chip {
    background: linear-gradient(155deg, rgba(12,17,35,0.3) 0%, rgba(16,22,44,0.2) 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 16px 22px;
    flex: 1; min-width: 80px;
    text-align: center;
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1);
    animation: flowIn 0.5s ease-out;
    backdrop-filter: blur(32px) saturate(1.3);
}
.metric-chip:hover {
    border-color: rgba(99,102,241,0.15);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 8px 32px rgba(99,102,241,0.06);
}
.metric-num { font-size: 1.6rem; font-weight: 800; color: #818cf8; font-family: 'Space Grotesk', sans-serif; text-shadow: 0 0 24px rgba(129,140,248,0.25); }
.metric-lbl { font-size: 0.62rem; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }

/* ═══ LIQUID BUTTONS ═══ */
.stButton > button {
    border-radius: 16px !important;
    font-weight: 600 !important;
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1) !important;
    letter-spacing: 0.02em !important;
    backdrop-filter: blur(12px) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(150deg, #4338ca, #6366f1, #818cf8, #6366f1) !important;
    background-size: 300% 300% !important;
    animation: iridescent 5s ease infinite !important;
    border: none !important;
    box-shadow: 0 6px 28px rgba(99,102,241,0.3), 0 0 70px rgba(99,102,241,0.08) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 10px 44px rgba(99,102,241,0.4), 0 0 100px rgba(99,102,241,0.12) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(12,17,35,0.7) !important;
    border: 1px solid rgba(139,92,246,0.2) !important;
    color: #c4b5fd !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(139,92,246,0.06) !important;
    border-color: rgba(139,92,246,0.35) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(139,92,246,0.12), 0 0 50px rgba(139,92,246,0.04) !important;
}

/* ═══ LIQUID INPUTS ═══ */
textarea, .stTextInput > div > div > input {
    background: rgba(8,12,26,0.4) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #e2e8f0 !important;
    border-radius: 16px !important;
    transition: all 0.5s cubic-bezier(0.22,1,0.36,1) !important;
    font-family: 'Inter', sans-serif !important;
    backdrop-filter: blur(30px) saturate(1.3) !important;
}
textarea:focus, .stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.35) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.06), 0 0 48px rgba(99,102,241,0.04) !important;
}

/* ═══ LIQUID TABS ═══ */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 6px;
    border-bottom: 1px solid rgba(148,163,184,0.05) !important;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 14px 14px 0 0 !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    color: #475569 !important;
    transition: all 0.5s ease !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.05) !important;
    color: #818cf8 !important;
    border-bottom: 2px solid #6366f1 !important;
    text-shadow: 0 0 24px rgba(99,102,241,0.25) !important;
}

/* ═══ LIQUID SIDEBAR ═══ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(6,10,22,0.45) 0%, rgba(8,12,26,0.4) 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(36px) saturate(1.5) !important;
}

.stRadio > div { gap: 8px !important; }
.stRadio [data-testid="stMarkdownContainer"] p { font-size: 0.85rem !important; color: #94a3b8 !important; }
.stRadio [aria-checked="true"] + div p { color: #818cf8 !important; font-weight: 600 !important; text-shadow: 0 0 18px rgba(129,140,248,0.25) !important; }

/* ═══ LIQUID PROGRESS ═══ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4, #6366f1) !important;
    background-size: 300% 100% !important;
    animation: borderStream 3s linear infinite !important;
    border-radius: 99px !important;
    box-shadow: 0 0 18px rgba(99,102,241,0.25) !important;
}

hr { border-color: rgba(148,163,184,0.04) !important; }

/* ═══ LIQUID EXPANDERS ═══ */
.streamlit-expanderHeader {
    background: rgba(12,17,35,0.5) !important;
    border: 1px solid rgba(148,163,184,0.05) !important;
    border-radius: 16px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    transition: all 0.5s ease !important;
    backdrop-filter: blur(14px) !important;
}
.streamlit-expanderHeader:hover {
    border-color: rgba(99,102,241,0.15) !important;
    color: #e2e8f0 !important;
    box-shadow: 0 6px 24px rgba(99,102,241,0.04) !important;
}

[data-testid="stChatMessage"] {
    background: rgba(12,17,35,0.5) !important;
    border: 1px solid rgba(148,163,184,0.05) !important;
    border-radius: 18px !important;
    backdrop-filter: blur(14px) !important;
    animation: flowIn 0.4s ease-out !important;
}

/* ═══ LIQUID SCROLLBAR ═══ */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.15); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.3); }

/* ═══ SELECTION ═══ */
::selection { background: rgba(99,102,241,0.2); color: #e2e8f0; }

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
if "fc_report" not in st.session_state: st.session_state.fc_report = ""
if "dejargoned_text" not in st.session_state: st.session_state.dejargoned_text = ""
if "constructor_premises" not in st.session_state: st.session_state.constructor_premises = [""]
if "debate_messages" not in st.session_state: st.session_state.debate_messages = []

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
# Local logic engine deleted. UI is 100% powered by Gemini Native JSON format.
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
            snip = h.get("conclusions", [""])[0] if h.get('conclusions') else h.get('conclusion', "No conclusion")
            snip = str(snip)[:30]
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
    <div class='hero-badge'>✦ 100% Gemini Neural Engine</div>
    <div class='hero-title'>Argument Analyzer Pro</div>
    <div class='hero-sub'>Deconstruct fallacies, map logic, and stress-test arguments with pure AI intelligence.</div>
    <div class='hero-stats'>
        <div class='hero-stat'><div class='hero-stat-num'>∞</div><div class='hero-stat-lbl'>Depth Layers</div></div>
        <div class='hero-stat'><div class='hero-stat-num'>50+</div><div class='hero-stat-lbl'>Fallacy Types</div></div>
        <div class='hero-stat'><div class='hero-stat-num'>5</div><div class='hero-stat-lbl'>Input Modes</div></div>
        <div class='hero-stat'><div class='hero-stat-num'>∞</div><div class='hero-stat-lbl'>Languages</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_analyze, tab_compare, tab_construct, tab_debate = st.tabs(["🔍 Analyze", "⚖️ Comparison", "🧱 Constructor", "🗣️ Simulator"])

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
    src = st.radio("**Input Source**", ["✍️ Text", "🌐 Web URL", "📄 PDF File", "🎥 YouTube Video", "🎤 Audio Speech"], horizontal=True)
    source_text = st.text_area("", value=st.session_state.arg_input, height=150,
                               placeholder="Paste your argument here…", key="txt_input_main",
                               label_visibility="collapsed")

    if src == "🌐 Web URL":
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
    elif src == "🎥 YouTube Video":
        url = st.text_input("🎥 YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        if url:
            with st.spinner("Extracting video transcript…"):
                source_text = extract_text_from_youtube(url)
                if not source_text:
                    st.error("Could not fetch transcript. Ensure the video has English closed captions.")
                elif source_text.startswith("Error:"):
                    st.error(source_text)
                    source_text = ""

    elif src == "🎤 Audio Speech":
        audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])
        if audio_file:
            if not gemini_key:
                st.warning("Please enter your Gemini API Key in the sidebar (Audio processing requires Gemini Audio API).")
            else:
                with st.spinner("Transcribing audio verbatim using Native Gemini Audio AI…"):
                    source_text = transcribe_audio_with_gemini(gemini_key, audio_file.read(), audio_file.type)
                    if "Failed:" in source_text:
                        st.error(source_text)
                        source_text = ""
                    else:
                        st.success("Audio transcribed successfully!")
                        with st.expander("📝 View Audio Transcript"):
                            st.write(source_text)

    # ── Action Buttons ─────────────────────────────────────────────────────────
    st.markdown("")
    
    b1, b2, b3 = st.columns(3)
    with b1:
        run_ai = st.button("🤖 AI Deep Scan", use_container_width=True, type="primary")
    with b2:
        run_fc = st.button("🔎 Live Fact-Check", use_container_width=True)
    with b3:
        run_dejarg = st.button("📖 De-Jargonize", use_container_width=True)

    if run_ai:
        if not gemini_key: 
            st.warning("Please enter your Gemini API Key in the sidebar.")
        elif source_text and len(source_text) > 5:
            with st.spinner("Gemini Native Execution is building the Logic Map…"):
                try:
                    results = run_ai_full_pipeline(gemini_key, source_text)
                    st.session_state.results = results
                    st.session_state.analysis_done = True
                    st.session_state.fc_report = ""
                    st.session_state.ai_report = results.get('ai_report', '')
                    st.session_state.history.append(results)
                except Exception as e:
                    st.error(str(e))
        else: 
            st.warning("Please provide an argument first.")

    if run_fc:
        if not gemini_key: st.warning("Please enter your Gemini API Key in the sidebar.")
        elif source_text and len(source_text) > 5:
            with st.spinner("Extracting claims & cross-referencing real-world data with Gemini…"):
                try:
                    results = run_ai_full_pipeline(gemini_key, source_text)
                    st.session_state.results = results
                    st.session_state.analysis_done = True
                    st.session_state.ai_report = ""
                    fc_report = run_ai_fact_check(gemini_key, results['premises'])
                    st.session_state.fc_report = fc_report
                    st.session_state.history.append(results)
                except Exception as e:
                    st.error(str(e))
        else: st.warning("Please provide an argument first.")


    if run_dejarg:
        if not gemini_key: st.warning("Please enter your Gemini API Key in the sidebar.")
        elif source_text and len(source_text) > 5:
            with st.spinner("Translating extremely complex text into 5th-grade logic…"):
                st.session_state.dejargoned_text = run_ai_dejargonize(gemini_key, source_text)
        else: st.warning("Please provide an argument first.")
        
    if st.session_state.get("dejargoned_text"):
        with st.expander("📖 De-Jargonized Translation", expanded=True):
            st.info(st.session_state.dejargoned_text)

    # ── Results ────────────────────────────────────────────────────────────────
    if st.session_state.get("analysis_done"):
        res = st.session_state.results
        st.markdown("---")

        # --- QUICK NAVIGATION LINKS ---
        link_html = """
        <div style='display:flex;gap:12px;justify-content:center;margin-bottom:24px;flex-wrap:wrap'>
            <a href="#extracted-premises" class="glass-card" style="padding:6px 12px;text-decoration:none;font-size:0.8rem;color:#94a3b8;border-color:#334155;transition:all 0.2s">🧱 Premises</a>
            <a href="#fallacy-detection" class="glass-card" style="padding:6px 12px;text-decoration:none;font-size:0.8rem;color:#f87171;border-color:#7f1d1d;transition:all 0.2s">🚨 Fallacies</a>
            <a href="#devils-advocate" class="glass-card" style="padding:6px 12px;text-decoration:none;font-size:0.8rem;color:#fbbf24;border-color:#78350f;transition:all 0.2s">⚖️ Counter-Arguments</a>
            <a href="#ai-deep-scan" class="glass-card" style="padding:6px 12px;text-decoration:none;font-size:0.8rem;color:#06b6d4;border-color:#164e63;transition:all 0.2s">🤖 AI Deep Scan</a>
        </div>
        """
        st.markdown(link_html, unsafe_allow_html=True)
        
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
            conclusion_text = res.get('conclusions', [""])[0] if res.get('conclusions') else res.get('conclusion', "")
            if conclusion_text:
                st.markdown(f"""<div class='conclusion-card'>
                    <div class='conclusion-label'>Main Claim</div>
                    <div class='conclusion-text'>{conclusion_text}</div>
                </div>""", unsafe_allow_html=True)
                st.markdown("<div style='margin-top:12px;display:inline-block;padding:4px 12px;background:#1e293b;border-radius:20px;border:1px solid #334155;font-size:0.75rem;color:#818cf8;font-weight:600;letter-spacing:0.05em'>AI EXTRACTED CONCLUSION</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='glass-card' style='color:#64748b;text-align:center'>No explicit conclusion detected.</div>", unsafe_allow_html=True)

            # Premises
            st.markdown("<div id='extracted-premises' class='section-header' style='margin-top:20px'><div class='section-icon'>📋</div><div class='section-title'>Supporting Premises</div></div>", unsafe_allow_html=True)
            if res['premises']:
                for i, p in enumerate(res['premises'], 1):
                    st.markdown(f"""<div class='premise-card'>
                        <div class='premise-num'>{i}</div>
                        <div class='premise-text'>{p}</div>
                    </div>""", unsafe_allow_html=True)
                
                # Render Fact-Check Report if active
                if st.session_state.get("fc_report"):
                    st.markdown(f"<div class='glass-card' style='border-color:#06b6d4;border-width:2px;margin-top:14px'><div style='font-size:0.75rem;font-weight:800;color:#06b6d4;letter-spacing:0.1em;margin-bottom:8px'>FACT-CHECK VERDICT</div>{st.session_state.fc_report}</div>", unsafe_allow_html=True)
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
                st.markdown("<div id='fallacy-detection' class='section-header'><div class='section-icon'>🚫</div><div class='section-title'>Logical Fallacies</div></div>", unsafe_allow_html=True)
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
            st.markdown("<div id='devils-advocate' style='color:#a78bfa;font-size:0.85rem;margin-bottom:16px;'>These AI-generated challenges help you pressure-test your logic before anyone else does.</div>", unsafe_allow_html=True)
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
                st.markdown(f"""<div id='ai-deep-scan' class='ai-report'>
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

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — DEBATE SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab_debate:
    st.markdown("<div class='section-header'><div class='section-icon'>🥊</div><div class='section-title'>AI Debate Simulator</div></div>", unsafe_allow_html=True)
    
    cd_col1, cd_col2 = st.columns([4,1])
    with cd_col1:
        st.markdown("<div style='color:#a78bfa;font-size:0.88rem;margin-bottom:20px'>Face off against a ruthless AI champion debater. Avoid logical fallacies, or you will be sharply penalized. State your opening argument below!</div>", unsafe_allow_html=True)
    with cd_col2:
        if st.button("🗑️ Reset Debate", use_container_width=True):
            st.session_state.debate_messages = []
            st.rerun()

    # Render History
    for msg in st.session_state.debate_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if debate_prompt := st.chat_input("Enter your argument (e.g., 'Nuclear energy is too dangerous because...'):"):
        if not gemini_key:
            st.warning("Please enter your Gemini API Key in the sidebar to debate.")
        else:
            # Display user msg instantly
            st.session_state.debate_messages.append({"role": "user", "content": debate_prompt})
            with st.chat_message("user"):
                st.markdown(debate_prompt)
                
            context_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.debate_messages[:-1]])
            
            # Fetch AI Reply
            with st.chat_message("assistant"):
                with st.spinner("AI is countering your logic..."):
                    ai_reply = run_ai_debate_response(gemini_key, context_str, debate_prompt)
                st.markdown(ai_reply)
            
            st.session_state.debate_messages.append({"role": "assistant", "content": ai_reply})

