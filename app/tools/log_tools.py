from app.models.schemas import LogEvent


def find_errors(events: list[LogEvent]) -> list[LogEvent]:
    return [
        event
        for event in events
        if event.level.upper() in {"ERROR", "CRITICAL", "FATAL"}
    ]


def find_warnings(events: list[LogEvent]) -> list[LogEvent]:
    return [
        event
        for event in events
        if event.level.upper() == "WARNING"
    ]


def find_events_for_service(
    events: list[LogEvent],
    service: str,
) -> list[LogEvent]:
    return [
        event
        for event in events
        if event.service.lower() == service.lower()
    ]


def search_logs(
    events: list[LogEvent],
    keyword: str,
) -> list[LogEvent]:
    keyword = keyword.lower()

    return [
        event
        for event in events
        if keyword in event.message.lower()
        or keyword in event.service.lower()
    ]


def count_log_levels(events: list[LogEvent]) -> dict[str, int]:
    counts: dict[str, int] = {}

    for event in events:
        level = event.level.upper()
        counts[level] = counts.get(level, 0) + 1

    return counts