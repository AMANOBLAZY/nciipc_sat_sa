import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="NCIIPC SAT-SA Dashboard", layout="wide")

st.title("🛡️ Supervisory Analytics Tool for SOC Assessment (SAT-SA)")
st.markdown("### Identifying Execution Gaps & Negative Space in Critical Sector Entities")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('analyzed_alerts.csv')

df = load_data()
anomalies = df[df['prediction'] == -1]

# Top level metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Alerts Analyzed", len(df))
col2.metric("Execution Gaps Detected", len(anomalies))
col3.metric("Entities Monitored", df['entity_id'].nunique())

st.divider()

# Layout
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🚨 Detected Execution Gaps")
    st.write("Alerts exhibiting abnormal operational behavior (e.g., closed too quickly or lacking escalation).")
    
    # Simple Explainability Logic (Rule-based XAI proxy for prototype)
    def explain_anomaly(row):
        reasons = []
        if row['severity'] in ['High', 'Critical'] and row['time_to_close_mins'] < 15:
            reasons.append("Critical alert closed unusually fast.")
        if row['severity'] in ['High', 'Critical'] and not row['escalated']:
            reasons.append("High severity without escalation.")
        if len(str(row['analyst_notes'])) < 30:
            reasons.append("Template/boilerplate note detected.")
        return " | ".join(reasons) if reasons else "Statistical Outlier"

    # Avoid SettingWithCopyWarning by creating a direct copy of the slice
    anomalies = anomalies.copy()
    anomalies['AI_Rationale'] = anomalies.apply(explain_anomaly, axis=1)
    
    display_df = anomalies[['entity_id', 'severity', 'time_to_close_mins', 'AI_Rationale']]
    st.dataframe(display_df, use_container_width=True)

with right_col:
    st.subheader("📉 Negative Space (Entity Benchmarking)")
    st.write("Comparing alert volumes across peers to find missing telemetry or low activity.")
    
    # Group by entity to find negative space
    entity_counts = df['entity_id'].value_counts().reset_index()
    entity_counts.columns = ['Entity', 'Total Alerts']
    st.bar_chart(entity_counts.set_index('Entity'))

st.subheader("🔎 Deep Dive: Analyst Notes Inspection")
selected_entity = st.selectbox("Select Entity to review manual notes:", df['entity_id'].unique())
entity_data = df[(df['entity_id'] == selected_entity) & (df['prediction'] == -1)]

if not entity_data.empty:
    st.table(entity_data[['alert_id', 'severity', 'analyst_notes', 'escalated']])
else:
    st.success("No execution gaps found for this entity.")