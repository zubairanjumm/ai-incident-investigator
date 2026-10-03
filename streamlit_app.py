import streamlit as st

from app.main import investigate


st.set_page_config(
    page_title="AI Incident Investigator",
    page_icon="🔎",
    layout="wide",
)


st.title("AI Incident Investigator")
st.caption(
    "Investigate application incidents using logs, evidence correlation, "
    "hypothesis generation, and AI-assisted root-cause analysis."
)

st.divider()


left, right = st.columns([1, 1])


with left:
    st.subheader("Incident")

    incident_description = st.text_area(
        "Incident description",
        placeholder=(
            "Example: Payment requests are intermittently failing "
            "during periods of high traffic."
        ),
        height=180,
    )


with right:
    st.subheader("Application Logs")

    uploaded_file = st.file_uploader(
        "Upload a log file",
        type=["log", "txt"],
    )

    logs = ""

    if uploaded_file:
        logs = uploaded_file.read().decode("utf-8")

    else:
        logs = st.text_area(
            "Or paste logs",
            placeholder=(
                "2026-10-03 12:01:00 INFO payment-api "
                "Payment request received\n"
                "2026-10-03 12:01:01 INFO payment-api "
                "Processing payment\n"
                "2026-10-03 12:01:02 ERROR payment-api "
                "Database connection timeout"
            ),
            height=180,
        )


st.divider()


run_investigation = st.button(
    "Run Investigation",
    type="primary",
    use_container_width=True,
)


if run_investigation:

    if not incident_description.strip():
        st.error("Enter an incident description.")
        st.stop()

    if not logs.strip():
        st.error("Upload or paste application logs.")
        st.stop()

    with st.spinner("Investigating incident..."):
        try:
            result = investigate(
                incident_description=incident_description,
                raw_logs=logs,
            )

        except Exception as exc:
            st.error("Investigation failed.")
            st.exception(exc)
            st.stop()

    report = result.get("report")

    if not report:
        st.error("The investigation did not produce a report.")
        st.stop()

    st.success("Investigation completed.")

    st.divider()

    st.subheader("Investigation Result")

    metric1, metric2 = st.columns(2)

    with metric1:
        st.metric(
            "Classification",
            report.classification,
        )

    with metric2:
        st.metric(
            "Confidence",
            f"{report.confidence:.0%}",
        )

    st.subheader("Issue Summary")
    st.write(report.issue_summary)

    st.subheader("Likely Root Cause")
    st.write(report.likely_root_cause)

    st.subheader("Supporting Evidence")

    if report.evidence:
        for evidence in report.evidence:
            st.code(evidence, language="text")
    else:
        st.info("No supporting evidence was returned.")

    st.subheader("Recommended Actions")

    if report.recommended_actions:
        for index, action in enumerate(
            report.recommended_actions,
            start=1,
        ):
            st.write(f"{index}. {action}")

    else:
        st.info("No recommended actions were returned.")


with st.expander("How the investigation works"):
    st.markdown(
        """
        1. **Parse logs** — Convert raw log lines into structured events.
        2. **Detect patterns** — Identify suspicious errors and warnings.
        3. **Correlate events** — Connect related evidence.
        4. **Generate hypotheses** — Use the AI model to propose possible causes.
        5. **Investigate hypotheses** — Search the available evidence.
        6. **Determine root cause** — Produce a structured incident report.
        """
    )
