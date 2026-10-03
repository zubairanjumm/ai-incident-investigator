import re

from app.models.schemas import LogEvent


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+\s+\S+)\s+"
    r"(?P<level>\w+)\s+"
    r"(?P<service>\S+)\s+"
    r"(?P<message>.*)$"
)


def parse_log_line(line: str) -> LogEvent | None:
    line = line.strip()

    if not line:
        return None

    match = LOG_PATTERN.match(line)

    if not match:
        return None

    data = match.groupdict()

    return LogEvent(
        timestamp=data["timestamp"],
        level=data["level"],
        service=data["service"],
        message=data["message"],
        raw=line,
    )


def parse_logs(log_text: str) -> list[LogEvent]:
    events = []

    for line in log_text.splitlines():
        event = parse_log_line(line)

        if event:
            events.append(event)

    return events