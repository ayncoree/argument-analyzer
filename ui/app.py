"""
ui/app.py — Next-Gen Argument Analyzer UI (V2)

Features:
- Multi-source input: Text, URL, PDF
- Comparison Mode: Analyzes two arguments side-by-side
- Sentiment/Tone Dashboard: Visualizing Objective vs. Aggressive tone
- Premium Glassmorphism UI
"""

import json
import datetime
import streamlit as st
import pandas as pd

from analyzer.parser import split_sentences, extract_text_from_url, extract_text_from_pdf
from analyzer.classifier import (
    detect_conclusion_with_confidence,
    extract_premises,
    analyse_tone,
    compute_argument_strength,
)
from analyzer.fallacies import detect_all_fallacies
from analyzer.objections import detect_counter_arguments, generate_devils_advocate_rebuttals

# ──────────────────────────────────────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Argument Analyzer Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS — deep dark, glassmorphism, premium typography
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif !important; background-color: #080c14 !important; color: #e2e8f0 !important; }
#MainMenu, footer, header { visibility: hidden; }
.hero { background: linear-gradient(135deg, #0f1e3a 0%, #111827 40%, #0f172a 100%); border: 1px solid rgba(91,143,249,0.18); border-radius: 20px; padding: 20px 30px; margin-bottom: 28px; }
.hero-title { font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #ffffff 0%, #93c5fd 60%, #a78bfa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.glass-card { background: rgba(15,23,42,0.7); border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 18px 20px; margin-bottom: 12px; }
.tone-label { font-weight: 700; font-size: 1.2rem; margin-top: 10px; text-align: center; }
textarea, .stTextInput > div > div > input { background: rgba(15,23,42,0.9) !important; border: 1px solid rgba(91,143,249,0.2) !important; color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

def run_analysis_pipeline(text: str, label_prefix: str = ""):
    """Centralized analysis logic for single or comparison mode."""
    sentences = split_sentences(text)
    conclusion, confidence, _ = detect_conclusion_with_confidence(sentences)
    premises = extract_premises(sentences, conclusion) if conclusion else []
    fallacies = detect_all_fallacies(sentences, conclusion)
    objections = detect_counter_arguments(sentences, conclusion, premises)
    devils_advocate = generate_devils_advocate_rebuttals(premises)
    tone = analyse_tone(sentences)
    score, str_label = compute_argument_strength(conclusion, premises, fallacies, objections)

    return {
        "text": text,
        "sentences": sentences,
        "conclusion": conclusion,
        "confidence": confidence,
        "premises": premises,
        "fallacies": fallacies,
        "objections": objections,
        "devils_advocate": devils_advocate,  # New field
        "tone": tone,
        "score": score,
        "str_label": str_label
    }

# ──────────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Engine Options")
    show_graph = st.checkbox("Show Graph", value=True)
    show_raw_source = st.checkbox("Display Raw Source", value=False)
    st.markdown("---")
    st.markdown("### 📜 Export Results")
    if "results" in st.session_state:
        st.download_button("JSON Export", data=json.dumps(st.session_state.results, default=str), file_name="argument_analysis.json")

# ──────────────────────────────────────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero"><div class="hero-title">🧠 Argument Analyzer Pro</div><div style="color:#64748b">Advanced Logical Deconstruction Engine v2.0</div></div>""", unsafe_allow_html=True)

tab_analyze, tab_compare, tab_construct = st.tabs(["🔍 Analyze Single Source", "⚖️ Compare Arguments", "🧱 Argument Constructor"])

with tab_analyze:
    source_type = st.radio("Choose Input Type", ["Text", "URL", "PDF"], horizontal=True)
    source_text = ""

    if source_type == "Text":
        source_text = st.text_area("Paste Argument Here", height=150, key="txt_input")
    elif source_type == "URL":
        url = st.text_input("Enter Web URL", placeholder="https://www.nature.com/articles/...")
        if url:
            with st.spinner("Scraping Content..."):
                source_text = extract_text_from_url(url)
                if not source_text: st.error("Could not fetch data.")
    elif source_type == "PDF":
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf_file:
            with st.spinner("Reading PDF..."):
                source_text = extract_text_from_pdf(pdf_file)

    if st.button("🚀 Run Comprehensive Analysis", use_container_width=True):
        if not source_text or len(source_text) < 10:
            st.warning("No sufficient text detected.")
        else:
            with st.spinner("Decoding Logical Architecture..."):
                results = run_analysis_pipeline(source_text)
                st.session_state.results = results
                st.session_state.analysis_done = True

    if st.session_state.get("analysis_done"):
        res = st.session_state.results
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 🎯 Conclusion & Premises")
            if res['conclusion']:
                st.markdown(f"<div class='glass-card' style='border-left:5px solid #5B8FF9'><div style='font-size:0.8rem;color:#475569'>Main Claim</div><div style='font-size:1.1rem;font-weight:600'>{res['conclusion']}</div></div>", unsafe_allow_html=True)
                st.progress(res['confidence'], "Confidence")
            else: st.info("No conclusion detected.")

            st.markdown("#### Supporting Evidence")
            for i, p in enumerate(res['premises'], 1):
                st.markdown(f"**{i}.** {p}")

        with col2:
            st.markdown("### 💪 Argument Strength")
            st.markdown(f"<div class='glass-card' style='text-align:center'><div style='font-size:2.5rem;font-weight:800;color:#5AD8A6'>{res['score']}</div><div style='font-size:1.1rem;color:#64748b'>{res['str_label']}</div></div>", unsafe_allow_html=True)

            st.markdown("### 🎭 Tone Analysis")
            tone = res['tone']
            st.markdown(f"<div class='tone-label' style='color:{tone['color']}'>{tone['label']}</div>", unsafe_allow_html=True)
            # Use dataframes for a simple tone chart
            tone_data = pd.DataFrame({
                "Category": ["Aggressive", "Objective"],
                "Score": [tone['aggressive'], tone['objective']]
            })
            st.bar_chart(tone_data, x="Category", y="Score")

        st.divider()

        with st.expander("⚠️ Detected Fallacies & Objections", expanded=True):
            f_col, o_col = st.columns(2)
            with f_col:
                st.write("#### Fallacies")
                for f in res['fallacies']:
                    st.error(f"**{f['type']}**: {f['explanation']}")
            with o_col:
                st.write("#### Counter-Arguments")
                for o in res['objections']:
                    st.warning(f"**{o['type']}**: {o['sentence']}")

        st.divider()

        with st.expander("😈 Challenge Your Argument (Devil's Advocate)", expanded=True):
            st.info("The suggestions below are automatically generated to help you find weaknesses in your own logic.")
            for i, suggestion in enumerate(res['devils_advocate'], 1):
                st.markdown(f"**Insight {i}:** {suggestion}")

with tab_compare:
    c1, c2 = st.columns(2)
    with c1: arg1 = st.text_area("Argument A", height=150, key="arg1")
    with c2: arg2 = st.text_area("Argument B", height=150, key="arg2")

    if st.button("⚖️ Compare Side-By-Side", use_container_width=True):
        if arg1 and arg2:
            res1 = run_analysis_pipeline(arg1)
            res2 = run_analysis_pipeline(arg2)

            st.markdown("### Comparison Results")
            # Create a comparison dataframe
            comp_df = pd.DataFrame({
                "Metric": ["Strength Score", "Tone label", "Premises #", "Fallacies #", "Confidence %"],
                "Argument A": [res1['score'], res1['tone']['label'], len(res1['premises']), len(res1['fallacies']), int(res1['confidence']*100)],
                "Argument B": [res2['score'], res2['tone']['label'], len(res2['premises']), len(res2['fallacies']), int(res2['confidence']*100)]
            })
            st.table(comp_df)

            st.write("#### Tone Visual Comparison")
            # Construct comparison chart data
            tone_comp_data = pd.DataFrame({
                "Tone Type": ["Objective", "Aggressive", "Objective", "Aggressive"],
                "Source": ["Arg A", "Arg A", "Arg B", "Arg B"],
                "Score": [res1['tone']['objective'], res1['tone']['aggressive'], res2['tone']['objective'], res2['tone']['aggressive']]
            })
            st.bar_chart(tone_comp_data, x="Tone Type", y="Score", color="Source")

            cl1, cl2 = st.columns(2)
            with cl1:
                st.markdown(f"**Main Conclusion A**: {res1['conclusion']}")
                st.markdown("**Premises A**:")
                for p in res1['premises']: st.write(f"- {p}")
            with cl2:
                st.markdown(f"**Main Conclusion B**: {res2['conclusion']}")
                st.markdown("**Premises B**:")
                for p in res2['premises']: st.write(f"- {p}")

with tab_construct:
    st.markdown("### 🧱 Build Your Logic Chain")
    st.info("Manually construct your argument to ensure each premise leads logically to your conclusion.")

    if 'constructor_premises' not in st.session_state:
        st.session_state.constructor_premises = [""]

    def add_premise(): st.session_state.constructor_premises.append("")
    def remove_premise():
        if len(st.session_state.constructor_premises) > 1: st.session_state.constructor_premises.pop()

    st.markdown("#### Premises")
    for i in range(len(st.session_state.constructor_premises)):
        st.session_state.constructor_premises[i] = st.text_input(f"Premise {i+1}", value=st.session_state.constructor_premises[i], key=f"construct_p_{i}")

    p_col1, p_col2 = st.columns(2)
    with p_col1: st.button("➕ Add Premise", on_click=add_premise)
    with p_col2: st.button("➖ Remove Premise", on_click=remove_premise)

    st.markdown("#### Conclusion")
    constructor_conclusion = st.text_input("Define Your Main Claim", key="construct_c")

    if st.button("🛠 Validate Logic Builder", use_container_width=True):
        full_text = ". ".join(st.session_state.constructor_premises) + ". Therefore " + constructor_conclusion
        res = run_analysis_pipeline(full_text)

        # New: Leap of Faith / Gap detection
        conclusion_words = set(re.findall(r'\b[a-z]{4,}\b', constructor_conclusion.lower()))
        premise_words = set(re.findall(r'\b[a-z]{4,}\b', " ".join(st.session_state.constructor_premises).lower()))
        unsupported = conclusion_words - premise_words
        
        st.success(f"Logic Builder Results: Argument Strength is **{res['score']}** ({res['str_label']})")
        
        if unsupported and len(unsupported) > 1:
            st.warning(f"🚨 **Logic Gap Detected**: These terms in your conclusion are not mentioned in your premises: *{', '.join(unsupported)}*. This is a 'leap of faith'.")
        
        if res['fallacies']:
            st.warning("Potential logical errors detected in your structure.")
            for f in res['fallacies']: st.write(f"- {f['type']}")
        else:
            st.balloons()
            st.success("Structure is logically sound based on current rules!")
