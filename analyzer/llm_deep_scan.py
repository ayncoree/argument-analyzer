"""
llm_deep_scan.py — Bulletproof AI Deep Analysis Module

Updated with multi-model fallback to avoid 404 errors.
"""

import google.generativeai as genai
from typing import Optional
import os
import tempfile
import json
import re


def _call_gemini_fallback(api_key: str, prompt: str) -> str:
    """Internal helper to execute Gemini Generation with 404 Fallback logic."""
    try:
        genai.configure(api_key=api_key)
        
        # Try models in order of likelihood to work
        models_to_try = [
            'gemini-2.5-pro',
            'gemini-2.5-flash',
            'gemini-3-pro-preview',
            'gemini-2.0-flash'
        ]
        
        errors = {}
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text # Success!
            except Exception as e:
                errors[model_name] = str(e)
                continue
        
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception:
            available_models.append("Could not list models")
            
        error_msg = "**AI Scan Failed.** Tried the following models and all returned an error:\n\n"
        for m, err in errors.items():
            error_msg += f"- **{m}**: {err}\n"
            
        error_msg += f"\n**Available Models for your API Key:**\n{', '.join(available_models)}"
        return error_msg
        
    except Exception as e:
        return f"System configuration failed: {str(e)}"

def run_ai_deep_scan(api_key: str, text: str) -> Optional[str]:
    """Generates an advanced formal logic report for a single argument."""
    if not api_key: return "API Key Missing."
    prompt = f"""
    Analyze the following argument like a professor of formal logic. 
    Provide a structured response with:
    1. **Hidden Premises (Enthymemes)**: What is assumed but not stated?
    2. **Logical Form**: Deconstruct it into P -> Q or similar formal logic structure.
    3. **Subtle Biases**: Are there any underlying psychological biases present?
    4. **Structural Soundness**: A final verdict on soundness and validity.
    
    ARGUMENT:
    "{text}"
    """
    return _call_gemini_fallback(api_key, prompt)

def run_ai_compare(api_key: str, arg1: str, arg2: str) -> Optional[str]:
    """Acts as a Debate Judge to compare two conflicting arguments."""
    if not api_key: return "API Key Missing."
    prompt = f"""
    Act as a neutral Debate Judge and Formal Logic Professor. Compare these two arguments logically.
    Provide a structured response with:
    1. **Strongest Points of A**: Where is Argument A most logically sound?
    2. **Strongest Points of B**: Where is Argument B most logically sound?
    3. **Fatal Flaws**: Does either argument contain a fatal logical flaw or rely heavily on fallacies?
    4. **The Verdict**: Determine which argument is logically superior and why.
    
    ARGUMENT A:
    "{arg1}"
    
    ARGUMENT B:
    "{arg2}"
    """
    return _call_gemini_fallback(api_key, prompt)

def run_ai_constructor(api_key: str, constructor_text: str) -> Optional[str]:
    """Acts as a Logic Coach assessing a user's manually constructed syllogism."""
    if not api_key: return "API Key Missing."
    prompt = f"""
    Act as a Formal Logic Coach. A student has specifically constructed this premise-by-premise argument.
    Analyze their work step-by-step:
    1. **Leaps of Faith**: Do the premises actually lead strictly to the conclusion? Name the gap if not.
    2. **Counter-Attack**: If an opponent wanted to dismantle this, which exact premise would they attack first?
    3. **Advice**: Provide one specific suggestion to make this argument completely watertight.
    
    STUDENT'S ARGUMENT:
    "{constructor_text}"
    """
    return _call_gemini_fallback(api_key, prompt)

def run_ai_fact_check(api_key: str, premises: list) -> Optional[str]:
    """Acts as a rigorous Fact-Checking Engine to verify the Soundness of an argument."""
    if not api_key: return "API Key Missing."
    if not premises: return "No explicit premises were found to fact-check."
    
    premises_str = "\n".join([f"- {p}" for p in premises])
    prompt = f"""
    Act as a rigorous Fact-Checking API. Analyze the following specific claims.
    For each claim, determine if it is factually True, False, Misleading, or Unverifiable based on generally accepted real-world data and consensus.
    
    CLAIMS TO VERIFY:
    {premises_str}
    
    For each claim, provide:
    1. A clear Verdict tag: [🔴 FALSE], [🟡 MISLEADING], [🟢 TRUE], or [⚪ UNVERIFIABLE].
    2. A brief, 1-2 sentence explanation of why.
    """
    return _call_gemini_fallback(api_key, prompt)

def run_ai_debate_response(api_key: str, chat_context: str, latest_message: str) -> Optional[str]:
    """Acts as an elite Debater AI that actively engages the user in real-time."""
    if not api_key: return "System Error: API Key Missing."
    
    prompt = f"""
    Act as an elite, ruthless champion Debater. You are engaged in a rigorous 1-on-1 debate with the user.
    
    CONVERSATION CONTEXT SO FAR:
    {chat_context}
    
    THE USER'S LATEST POINT:
    "{latest_message}"
    
    Your task:
    1. **Call Out Fallacies**: If the user's latest point relies on a logical fallacy, name it explicitly and brutally point it out.
    2. **Counter-Attack**: Provide a sharp, logically sound counter-argument that dismantles their point.
    3. **The Pivot**: End your response by asking a piercing, difficult question that forces them to defend their stance.
    
    Your tone should be highly analytical, articulate, slightly challenging, but strictly focused on logic, not personal attacks.
    """
    return _call_gemini_fallback(api_key, prompt)

def run_ai_dejargonize(api_key: str, text: str) -> Optional[str]:
    """Simplifies complex text into a 5th-grade reading level while preserving core logic."""
    if not api_key: return "API Key Missing."
    prompt = f"""
    Act as an expert "De-Jargonator". The following text is overly complex, academic, or legalistic.
    Rewrite it so a 10-year-old (5th-grade level) can perfectly understand the core logical argument.
    Do not lose any important premises or the conclusion, but utterly destroy all jargon, $10 words, and convoluted phrasing.
    
    ORIGINAL TEXT:
    "{text}"
    """
    return _call_gemini_fallback(api_key, prompt)

def transcribe_audio_with_gemini(api_key: str, file_bytes: bytes, mime_type: str) -> Optional[str]:
    """Uploads an audio file to Gemini and returns the verbatim transcript."""
    if not api_key: return "API Key Missing."
    try:
        genai.configure(api_key=api_key)
        
        suffix = ".mp3" if "mp3" in mime_type else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
            
        try:
            audio_file = genai.upload_file(path=tmp_path)
            
            # Use the 2.5 pro model we verified to work
            model = genai.GenerativeModel('gemini-2.5-pro')
            prompt = "Please transcribe the following audio verbatim. Provide only the text."
            response = model.generate_content([audio_file, prompt])
            
            try:
                genai.delete_file(audio_file.name)
            except Exception:
                pass
                
            return response.text
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
                
    except Exception as e:
        return f"Audio Transcription Failed: {str(e)}"

def run_ai_full_pipeline(api_key: str, text: str) -> dict:
    """The Ultimate Gemini Master Engine. Replaces all local processing by generating flawless formatted JSON logic outputs."""
    if not api_key: raise ValueError("Gemini API Key Missing. The app relies 100% on the neural network now.")
    prompt = f"""
    Act as a Master Logician. Analyze the following argument and output ONLY valid JSON.
    DO NOT output Markdown code blocks (like ```json), DO NOT output any conversational text.
    Your entire response MUST be a parseable JSON object exactly matching this schema:
    
    {{
      "conclusions": ["The main conclusion of the text"],
      "premises": ["Premise 1", "Premise 2", "Premise 3"],
      "fallacies": [{{"type": "Name of Fallacy", "explanation": "Why it occurred", "severity": "high"}}],
      "objections": [{{"type": "Type of counter", "explanation": "Why this attacks the logic", "sentence": "The original premise being attacked"}}],
      "devils_advocate": ["Challenge 1", "Challenge 2"],
      "tone": {{"label": "Objective", "color": "#06b6d4", "objective": 80, "aggressive": 10}},
      "score": 85,
      "str_label": "Strongly Supported",
      "ai_report": "A 2-paragraph formal logic markdown analysis."
    }}
    
    TEXT:
    "{text}"
    """
    raw = _call_gemini_fallback(api_key, prompt)
    
    # Clean up formatting anomalies where Gemini disobeys "no codeblocks"
    clean_json = re.sub(r'(?i)```json\n|\n```|```', '', raw).strip()
    
    try:
        data = json.loads(clean_json)
        # Type guarding default fields
        for key in ["conclusions", "premises", "fallacies", "objections", "devils_advocate"]:
            if key not in data: data[key] = []
        if "tone" not in data: data["tone"] = {"label": "Neutral", "color": "#94a3b8", "objective": 50, "aggressive": 0}
        if "score" not in data: data["score"] = 50
        if "str_label" not in data: data["str_label"] = "Unknown Validation"
        if "ai_report" not in data: data["ai_report"] = "No formal logic report generated."
        return data
    except Exception as e:
        raise ValueError(f"Failed to parse Native UI JSON Pipeline. Raw Output: {raw}")

