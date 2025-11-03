from typing import Dict, Any
import openai
import os

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def _get_creativity_score(prompt: str) -> float:
    if not OPENAI_KEY:
        return 0.0
    
    client = openai.OpenAI(api_key=OPENAI_KEY)
    
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Rate the creativity of the following prompt on a scale of 1 to 10, where 1 is not creative and 10 is highly creative. Only return the number.\n\nPrompt: {prompt}\n\nCreativity Score:",
        max_tokens=5,
        temperature=0.5,
        n=1
    )
    
    try:
        return float(response.choices[0].text.strip())
    except (ValueError, IndexError):
        return 0.0

def heuristic_score_variant(variant_prompt: str, base_prompt: str) -> Dict[str, Any]:
    words = len(variant_prompt.split())
    base_words = len(base_prompt.split())
    length_score = max(0, 10 - abs(words - base_words) / max(1, base_words) * 10)
    role_bonus = 1 if any(word in variant_prompt.lower() for word in ["assume","you are","expert","role"]) else 0
    format_bonus = 1 if any(x in variant_prompt for x in ["JSON","markdown","table","csv"]) else 0
    clarity = min(10, length_score + role_bonus + format_bonus)
    creativity = min(10, _get_creativity_score(variant_prompt))
    overall = round((clarity * 0.6 + creativity * 0.4), 2)
    return {
        "length_words": words,
        "clarity": round(clarity,2),
        "creativity": round(creativity,2),
        "overall": overall
    }

def score_variants(variants, base_prompt: str):
    scored = []
    for v in variants:
        p = v["prompt"]
        scores = heuristic_score_variant(p, base_prompt)
        scored.append({**v, "scores": scores})
    return scored
