from typing import TypedDict

from app.agents.correlator import correlate_events
from app.agents.hypothesis_generator import generate_hypotheses
from app.agents.investigator import investigate_hypothesis
from app.agents.pattern_detector import detect_patterns
from app.agents.root_cause import determine_root_cause
from app.models.schemas import (
    CorrelatedEvent,
    Hypothesis,
    IncidentReport,
    InvestigationResult,
    LogEvent,
    SuspiciousPattern,
)
from app.parsers.log_parser import parse_logs


class InvestigationState(TypedDict, total=False):
    incident_description: str
    raw_logs: str
    events: list[LogEvent]
    patterns: list[SuspiciousPattern]
    correlations: list[CorrelatedEvent]
    hypotheses: list[Hypothesis]
    investigations: list[InvestigationResult]
    report: IncidentReport


def parse_logs_node(state: InvestigationState):
    events = parse_logs(state["raw_logs"])

    return {
        "events": events,
    }


def detect_patterns_node(state: InvestigationState):
    patterns = detect_patterns(state["events"])

    return {
        "patterns": patterns,
    }


def correlate_events_node(state: InvestigationState):
    correlations = correlate_events(
        state["events"],
        state["patterns"],
    )

    return {
        "correlations": correlations,
    }


def generate_hypotheses_node(state: InvestigationState):
    hypotheses = generate_hypotheses(
        state["patterns"],
        state["correlations"],
    )

    return {
        "hypotheses": hypotheses,
    }


def investigate_node(state: InvestigationState):
    investigations = []

    for hypothesis in state["hypotheses"]:
        result = investigate_hypothesis(
            hypothesis,
            state["events"],
            state["correlations"],
        )

        investigations.append(result)

    return {
        "investigations": investigations,
    }


def root_cause_node(state: InvestigationState):
    report = determine_root_cause(
        state["incident_description"],
        state["hypotheses"],
        state["investigations"],
    )

    return {
        "report": report,
    }


def build_workflow():
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(InvestigationState)

    graph.add_node("parse_logs", parse_logs_node)
    graph.add_node("detect_patterns", detect_patterns_node)
    graph.add_node("correlate_events", correlate_events_node)
    graph.add_node("generate_hypotheses", generate_hypotheses_node)
    graph.add_node("investigate", investigate_node)
    graph.add_node("root_cause", root_cause_node)

    graph.add_edge(START, "parse_logs")
    graph.add_edge("parse_logs", "detect_patterns")
    graph.add_edge("detect_patterns", "correlate_events")
    graph.add_edge("correlate_events", "generate_hypotheses")
    graph.add_edge("generate_hypotheses", "investigate")
    graph.add_edge("investigate", "root_cause")
    graph.add_edge("root_cause", END)

    return graph.compile()