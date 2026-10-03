from app.graph.workflow import build_workflow


def investigate(
    incident_description: str,
    raw_logs: str,
):
    workflow = build_workflow()

    result = workflow.invoke(
        {
            "incident_description": incident_description,
            "raw_logs": raw_logs,
        }
    )

    return result