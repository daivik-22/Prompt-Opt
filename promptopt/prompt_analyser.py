from typing import Dict, Any, List
import re

def analyze_prompt(prompt: str) -> Dict[str, Any]:
    words = prompt.split()
    length = len(words)
    sentences = re.split(r'[.!?]\s*', prompt.strip())
    sentences = [s for s in sentences if s]
    question_marks = prompt.count('?')
    has_role = bool(re.search(r'\b(you are|assume|as a)\b', prompt, re.I))
    has_examples = bool(re.search(r'example|for example|e\.g\.', prompt, re.I))
    has_format = bool(re.search(r'JSON|markdown|table|csv', prompt, re.I))
    ambiguous_words = [w for w in ['maybe','perhaps','some','could','possibly','might'] if w in prompt.lower()]

    issues = []
    if length < 3:
        issues.append("Prompt is very short — likely underspecified.")
    if length > 120:
        issues.append("Prompt is long — consider concise framing or bullet points.")
    if question_marks > 1 and not prompt.strip().endswith('?'):
        issues.append("Multiple questions detected — split into separate prompts if needed.")
    if not has_role:
        issues.append("No role/context defined — consider using 'You are' or 'Assume' for role priming.")
    if not has_examples:
        issues.append("No examples present — add few-shot examples to control style/output if needed.")
    if ambiguous_words:
        issues.append(f"Ambiguous words found: {', '.join(ambiguous_words)}")

    score_est = max(0, min(10, 10 - (len(issues) * 2) + (0 if length<10 else 1)))

    return {
        "length_words": length,
        "sentences": len(sentences),
        "question_marks": question_marks,
        "has_role": has_role,
        "has_examples": has_examples,
        "has_format_directive": has_format,
        "issues": issues,
        "estimated_quality_score": score_est
    }
