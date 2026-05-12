from soc_analyser_helper import analyze_logs
import streamlit as st

st.title("AI SOC Analyst Agent")

logs = st.text_area("Enter security logs for analysis:")

if st.button("Analyze Logs"):
    if logs:
        analysis_result = analyze_logs(logs)
        st.subheader("Analysis Result:")
        st.text(analysis_result)
    else:
        st.warning("Please enter security logs for analysis.")