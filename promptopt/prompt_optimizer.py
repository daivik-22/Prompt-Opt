from typing import List, Dict, Optional
from .prompt_analyzer import analyze_prompt
import os
import openai
import json
import re

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def _local_rewrites(prompt: str, n: int = 4) -> List[Dict]:
    variants = []
    concise = "Rewrite concisely: " + prompt
    variants.append({"style": "concise", "prompt": concise})
    detailed = "Rewrite with more context and explicit instructions: " + prompt
    variants.append({"style": "detailed", "prompt": detailed})
    role = f"Assume you are an expert. {prompt}"
    variants.append({"style": "role:expert", "prompt": role})
    formatted = prompt + " Provide output in JSON with keys: result, summary."
    variants.append({"style": "json-format", "prompt": formatted})
    return variants[:n]

def _openai_rewrite(prompt: str, n: int = 3, model: str = "gpt-4o-mini") -> List[Dict]:
    if not OPENAI_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = OPENAI_KEY
    system = "You are a prompt engineering assistant. Produce improved prompt variants and a short rationale."
    template = (
        "Input prompt:\n'''\n{prompt}\n'''\n\n"
        "Produce {n} improved prompt variants. For each variant provide:\n"
        "- variant_prompt\n- tag (concise/detailed/role-based/creative/structured)\n"
        "- short rationale (one sentence)\n\nReturn a JSON array of objects."
    ).format(prompt=prompt, n=n)

    client = openai.OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system", "content": system},
            {"role":"user", "content": template}
        ],
        max_tokens=800,
        temperature=0.7,
        n=1
    )
    text = response.choices[0].message.content
    m = re.search(r'(\[.*\])', text, re.S)
    if m:
        try:
            parsed = json.loads(m.group(1))
            return parsed
        except Exception:
            pass
    return _local_rewrites(prompt)

def optimize_prompt(prompt: str, engine: str = "local", n: int = 3, model: str = "gpt-4o-mini") -> Dict:
    analysis = analyze_prompt(prompt)
    if engine == "local":
        variants = _local_rewrites(prompt, n=n)
    elif engine == "openai":
        try:
            variants = _openai_rewrite(prompt, n=n, model=model)
        except openai.APIError as e:
            variants = _local_rewrites(prompt)[:n]
            variants = [{"style":"fallback","prompt":v["prompt"], "rationale": f"OpenAI API error: {e}"} for v in variants]
    else:
        raise ValueError("Unknown engine")
    return {"analysis": analysis, "variants": variants}
