import json

from app.llm.client import generate_text
from app.models.schemas import (
    CorrelatedEvent,
    Hypothesis,
    SuspiciousPattern,
)


def generate_hypotheses(
    incident_description: str,
    patterns: list[SuspiciousPattern],
    correlations: list[CorrelatedEvent],
) -> list[Hypothesis]:
    pattern_data = [
        {
            "type": pattern.pattern_type,
            "description": pattern.description,
            "severity": pattern.severity,
            "evidence": pattern.evidence,
        }
        for pattern in patterns
    ]

    correlation_data = [
        {
            "description": correlation.description,
            "events": correlation.events,
            "relationship": correlation.relationship,
        }
        for correlation in correlations
    ]

    prompt = f"""
You are an incident investigation analyst.

Incident description:
{incident_description}

Suspicious patterns:
{json.dumps(pattern_data, indent=2)}

Correlated events:
{json.dumps(correlation_data, indent=2)}

Generate 1 to 3 plausible root-cause hypotheses.

Rules:
- Base hypotheses only on the supplied evidence.
- Do not invent infrastructure metrics or events.
- Each hypothesis must explain why the evidence supports it.
- Confidence must be between 0 and 1.

Return ONLY valid JSON using this structure:

[
  {{
    "title": "short hypothesis title",
    "explanation": "why this could explain the incident",
    "supporting_evidence": ["evidence 1", "evidence 2"],
    "confidence": 0.0
  }}
]
"""

    response = generate_text(prompt)

    try:
        data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON: {response}"
        ) from exc

    return [
        Hypothesis.model_validate(item)
        for item in data
    ]