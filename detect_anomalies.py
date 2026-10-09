import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

print("Loading SOC data...")
df = pd.read_csv('soc_alerts.csv')

# 1. Feature Engineering: Convert text columns to numbers so the ML model can understand them
print("Preprocessing features...")
le_severity = LabelEncoder()
df['severity_encoded'] = le_severity.fit_transform(df['severity'])

le_entity = LabelEncoder()
df['entity_encoded'] = le_entity.fit_transform(df['entity_id'])

# We will look at how long it took to close, how severe it was, whether it was escalated, and which entity it is.
features = ['time_to_close_mins', 'severity_encoded', 'escalated', 'entity_encoded']
X = df[features]

# 2. Train the Isolation Forest Model
# contamination=0.05 means we expect roughly 5% of our data to be anomalous (Execution Gaps)
print("Training Anomaly Detection Model (Isolation Forest)...")
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)

# 3. Predict Anomalies
# The model returns -1 for outliers (anomalies) and 1 for normal data
df['prediction'] = model.fit_predict(X)

# Filter out the anomalies
anomalies = df[df['prediction'] == -1]

print("-" * 50)
print(f"Total alerts analyzed: {len(df)}")
print(f"Suspicious alerts (Execution Gaps) detected: {len(anomalies)}")
print("-" * 50)
print("Top 5 most suspicious alerts flagged for Supervisory Review:\n")

# Display the most relevant columns for the supervisor
display_cols = ['entity_id', 'severity', 'time_to_close_mins', 'escalated', 'analyst_notes']
print(anomalies[display_cols].head())

# Save results for the next step (Dashboard)
df.to_csv('analyzed_alerts.csv', index=False)
print("\nSaved full analysis to 'analyzed_alerts.csv'")