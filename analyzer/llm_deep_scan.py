"""
llm_deep_scan.py — Bulletproof AI Deep Analysis Module

Updated with multi-model fallback to avoid 404 errors.
"""

import google.generativeai as genai
from typing import Optional

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
