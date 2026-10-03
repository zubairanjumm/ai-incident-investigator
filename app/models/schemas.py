from pydantic import BaseModel, Field


class LogEvent(BaseModel):
    timestamp: str
    level: str
    service: str
    message: str
    raw: str


class SuspiciousPattern(BaseModel):
    pattern_type: str
    description: str
    evidence: list[str] = Field(default_factory=list)
    severity: str


class CorrelatedEvent(BaseModel):
    description: str
    events: list[str] = Field(default_factory=list)
    relationship: str


class Hypothesis(BaseModel):
    title: str
    explanation: str
    supporting_evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class InvestigationResult(BaseModel):
    hypothesis: str
    findings: str
    supporting_evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class IncidentReport(BaseModel):
    classification: str
    confidence: float = Field(ge=0, le=1)
    issue_summary: str
    likely_root_cause: str
    evidence: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)