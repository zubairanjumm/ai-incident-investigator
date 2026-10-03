from app.models.schemas import LogEvent, SuspiciousPattern
from app.tools.log_tools import find_errors, find_warnings


def detect_patterns(
    events: list[LogEvent],
) -> list[SuspiciousPattern]:
    patterns = []

    errors = find_errors(events)

    if errors:
        patterns.append(
            SuspiciousPattern(
                pattern_type="error_spike",
                description=f"Found {len(errors)} error-level log events.",
                evidence=[event.raw for event in errors[:10]],
                severity="high",
            )
        )

    warnings = find_warnings(events)

    if len(warnings) >= 3:
        patterns.append(
            SuspiciousPattern(
                pattern_type="warning_cluster",
                description=f"Found {len(warnings)} warning events.",
                evidence=[event.raw for event in warnings[:10]],
                severity="medium",
            )
        )

    return patterns