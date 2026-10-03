from app.models.schemas import (
    CorrelatedEvent,
    LogEvent,
    SuspiciousPattern,
)


def correlate_events(
    events: list[LogEvent],
    patterns: list[SuspiciousPattern],
) -> list[CorrelatedEvent]:
    correlations = []

    for pattern in patterns:
        related_events = []

        for event in events:
            if event.raw in pattern.evidence:
                related_events.append(event.raw)

        if related_events:
            correlations.append(
                CorrelatedEvent(
                    description=pattern.description,
                    events=related_events,
                    relationship=f"Events support pattern: {pattern.pattern_type}",
                )
            )

    return correlations