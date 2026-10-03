from app.models.schemas import (
    Hypothesis,
    IncidentReport,
    InvestigationResult,
)


def determine_root_cause(
    incident_description: str,
    hypotheses: list[Hypothesis],
    investigations: list[InvestigationResult],
) -> IncidentReport:
    if not investigations:
        return IncidentReport(
            classification="Insufficient Evidence",
            confidence=0.20,
            issue_summary=incident_description,
            likely_root_cause="No sufficiently supported root-cause hypothesis was found.",
            evidence=[],
            recommended_actions=[
                "Collect more application logs.",
                "Investigate infrastructure and dependency metrics.",
            ],
        )

    best = max(
        investigations,
        key=lambda result: result.confidence,
    )

    return IncidentReport(
        classification=best.hypothesis,
        confidence=best.confidence,
        issue_summary=incident_description,
        likely_root_cause=best.findings,
        evidence=best.supporting_evidence,
        recommended_actions=[
            "Verify the suspected cause using application and infrastructure metrics.",
            "Check whether the same pattern appears in previous incidents.",
        ],
    )