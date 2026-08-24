# Prompt Shield

**Prompt Shield** is a hybrid AI input security gateway designed to protect Large Language Models (LLMs) and web applications from hostile inputs. It combines signature-based (regex) validation with a machine learning NLP classifier (TF-IDF + Logistic Regression) to filter prompt injections, jailbreaks, and standard web injection vectors (SQLi, XSS, and Command Injection).

The project features a decoupled **3-Port Security Architecture** separating the gateway API, security administration dashboard (SOC), and developer simulator playground.

---

## 3-Port Architecture & Port Map

*   **Port 5000: SOC Dashboard UI**
    A real-time security dashboard designed for analysts. It displays KPI metrics, logged security alerts, and tracks active rate-limiting or blocked constraints applied to offender IP addresses.
*   **Port 5001: AI Security Gateway API**
    The core analysis engine and stateful IP manager. It intercepts requests, extracts real client connection IPs, scores inputs (0-100), and blocks offending clients.
*   **Port 5002: Threat Simulator & Sandbox**
    An interactive simulation sandbox built for developers. You can select pre-mapped suggestion attacks or submit custom prompts to test the scanning gateway.

---

## Key Features

1.  **Hybrid Scanning Core**:
    *   *Signature Engine*: Scans inputs for structured regex patterns matching prompt attacks, jailbreaks, SQLi tautologies, HTML tags, and command chains.
    *   *Machine Learning Classifier*: Trains on normalized features to predict malicious intent probabilities.
2.  **Stateful IP Mitigation Policies**:
    *   *Cooldown Suspension*: The first malicious check triggers a **30-second cooldown suspension**. Further requests within this window are rejected with `429 Rate Limit Exceeded`.
    *   *Access Block*: Three consecutive infractions permanently upgrade the IP status to **Blocked**. Any future query from this client is rejected with `403 Access Denied`.
3.  **Analyst Controls**: Analysts can view active limits and manually unblock or reset restricted IP registries directly from the dashboard.
4.  **Decoupled CORS Design**: Cross-Origin Resource Sharing (CORS) preflights are implemented to permit secure, independent hosting of all three layers.

---

## Repository Index

*   `src/ai_server.py`: API Gateway (Port 5001) handling check routes, registry tracking, and logs.
*   `src/soc_server.py`: SOC UI Server (Port 5000) serving dashboard files.
*   `src/sandbox_server.py`: Threat Simulator Server (Port 5002) serving interactive playgrounds.
*   `src/regex_detector.py`: Regex rules engine identifying injection markers.
*   `src/ml_detector.py`: Model loader vectorizing and evaluating input using TF-IDF.
*   `src/risk_scorer.py`: Combines ML probability and regex rule counts to determine overall risk levels.
*   `src/train_ml_model.py`: Training script for model compilation and TF-IDF serialization.
*   `src/generate_dataset.py`: Generator scripting compiling the synthetic training set.
*   `data/promptshield_dataset.csv`: Compiled prompts dataset.
*   `data/dataset_schema.md`: Technical documentation of dataset structure.
*   `models/`: Serialized vectorizers and classifiers (`.joblib`).
*   `tests/`: Suite of unit tests written for `pytest`.

---

## Getting Started

### 1. Set Up Environment
Run in your Python environment:
```bash
# Create local virtual environment
python3 -m venv mac_env

# Activate and install packages
source mac_env/bin/activate
pip install -r requirements.txt
```

### 2. Generate Dataset & Train Model
To retrain or compile the ML engine with the latest rules:
```bash
# Compile dataset (XSS, SQLi, Prompt Injection, Cmd Injection)
python3 src/generate_dataset.py

# Train and serialize ML model
python3 src/train_ml_model.py
```

### 3. Spin Up Services
Run each service in separate terminal sessions:
```bash
# Start Gateway API (Port 5001)
python3 src/ai_server.py

# Start SOC Dashboard (Port 5000)
python3 src/soc_server.py

# Start Sandbox Simulator (Port 5002)
python3 src/sandbox_server.py
```

### 4. Running Automated Tests
```bash
pytest
```
