import json
import requests
from pydantic import BaseModel, Field

# 1. Define the exact structure we want the LLM to return
class AlertSummary(BaseModel):
    threat_level: str = Field(description="High, Medium, or Low")
    source_user: str = Field(description="The user who triggered the action")
    target_file: str = Field(description="The file or resource accessed")
    brief_explanation: str = Field(description="A short human-readable summary of what happened")

# 2. Sample raw JSON log mimicking what Falco outputs
sample_falco_alert = {
    "hostname": "dev-box",
    "priority": "Warning",
    "rule": "Sensitive file opened for reading",
    "output_fields": {
        "fd.name": "/etc/shadow",
        "user.name": "root",
        "proc.name": "cat"
    }
}

def generate_llm_summary(alert_dict: dict) -> str:
    """Sends the raw alert to local Ollama and requests a structured summary."""
class TriageReport(BaseModel):
    summary: str = Field(description="A concise 1-sentence summary of the alert.")
    threat_level: str = Field(description="Must be LOW, MEDIUM, or HIGH.")
    target_file: str = Field(description="The exact file path involved, extracted directly from the raw alert.")
    actor: str = Field(description="The username who performed the action.")

# 3. Craft a prompt explicitly requesting JSON format matching our schema
prompt = f"""
You are a SOC Triage Copilot. Analyze the following Falco security alert and output a valid JSON object ONLY, with these exact keys:
- "summary": A short 1-sentence description of the event.
- "threat_level": Either LOW, MEDIUM, or HIGH.
- "target_file": The file path found in the alert output fields.
- "actor": The username found in the alert output fields.

Raw Alert:
{json.dumps(sample_falco_alert, indent=2)}
"""

print("[*] Sending request to local LLM with structural constraints...")

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "qwen2.5:1.5b",  # Using your working lightweight model
    "prompt": prompt,
    "stream": False,
    "format": "json"  # Enforces JSON output at the Ollama engine level
})

result_json = response.json()
raw_ai_output = result_json.get("response", "{}")

print("\n[Raw AI JSON Output]:")
print(raw_ai_output)

# 4. Pydantic Validation Layer (Grounding Check)
print("\n[*] Running Pydantic Validation...")
try:
    # Parse the string into a Python dictionary, then validate via Pydantic
    parsed_data = json.loads(raw_ai_output)
    validated_report = TriageReport(**parsed_data)
    
    print("\n✅ SUCCESS: LLM output successfully validated and grounded!")
    print(validated_report.model_dump_json(indent=2))

except (json.JSONDecodeError, ValidationError) as e:
    print(f"\n❌ VALIDATION ERROR / HALLUCINATION DETECTED: {e}")
