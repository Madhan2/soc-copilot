# 🛡️ Grounded SOC Alert Triage Copilot

A lightweight, local-first AI security copilot designed to triage Falco runtime security alerts while preventing LLM hallucinations through deterministic Pydantic validation.

## 🏗️ Architecture & Approach
Security telemetry requires strict accuracy. Unchecked LLM summarization introduces hallucination risks (e.g., fabricating file paths or threat actors). This project bridges local runtime detection with generative AI safely:

1. **Detection:** Captures system anomalies and outputs structured JSON logs.
2. **Inference:** A local LLM (`qwen2.5:1.5b` via Ollama) analyzes the alert context and generates a structured summary.
3. **Deterministic Grounding:** Pydantic enforces structural schemas and type constraints, validating the AI's output before any automated action or dashboard display.

## 🚀 Tech Stack
* **Local LLM Engine:** Ollama (`qwen2.5:1.5b`)
* **Validation Layer:** Python & Pydantic
* **API Communication:** Requests

## 📂 Quickstart
1. Clone the repository and set up a virtual environment:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/soc-copilot.git](https://github.com/YOUR_USERNAME/soc-copilot.git)
   cd soc-copilot
   python3 -m venv venv
   source venv/bin/activate
   pip install pydantic requests
