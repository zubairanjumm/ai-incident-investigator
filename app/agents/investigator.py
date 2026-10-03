from app.models.schemas import (
    CorrelatedEvent,
    Hypothesis,
    InvestigationResult,
    LogEvent,
)
from app.tools.log_tools import search_logs


def investigate_hypothesis(
    hypothesis: Hypothesis,
    events: list[LogEvent],
    correlations: list[CorrelatedEvent],
) -> InvestigationResult:
    evidence = list(hypothesis.supporting_evidence)

    keywords = hypothesis.title.lower().split()

    for keyword in keywords:
        if len(keyword) < 4:
            continue

        matching_events = search_logs(events, keyword)

        for event in matching_events[:5]:
            if event.raw not in evidence:
                evidence.append(event.raw)

    return InvestigationResult(
        hypothesis=hypothesis.title,
        findings=hypothesis.explanation,
        supporting_evidence=evidence[:15],
        confidence=hypothesis.confidence,
    )