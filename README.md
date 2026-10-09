# 🛡️ NCIIPC SAT-SA: Supervisory Analytics Tool for SOC Assessment

## Problem Statement
The NCIIPC requires an offline, air-gapped **Supervisory Analytics Tool** to assess the cyber resilience of Critical Sector Entities (CSEs). This tool identifies **"Execution Gaps"** (e.g., critical alerts closed without investigation) and **"Negative Space"** (e.g., missing telemetry) in SOC case-management data without relying on external cloud APIs or SaaS platforms.

## Core Features
- **Air-Gapped Operation:** Runs 100% locally with no internet or cloud dependencies.
- **Unsupervised Machine Learning:** Utilizes Scikit-Learn (`IsolationForest`) to detect operational anomalies in analyst workflows.
- **Explainable AI (XAI):** Generates transparent, rule-based reasoning for every flagged anomaly so human supervisors can audit the findings.
- **Automated Benchmarking:** Compares entity alert volumes to detect missing telemetry (Negative Space).

## Setup Instructions (Local & Air-Gapped)

### Prerequisites
- Python 3.9+
- Pip (Python Package Installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/nciipc_sat_sa.git
   cd nciipc_sat_sa/data
   ```

2. **Create and activate a virtual environment:**
   * **Windows:**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   * **Mac/Linux:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install pandas numpy scikit-learn streamlit
   ```

### Execution

1. **Generate Mock Operational Data:**
   ```bash
   python generate_data.py
   ```

2. **Run Anomaly Detection Model:**
   ```bash
   python detect_anomalies.py
   ```

3. **Launch Supervisory Dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
