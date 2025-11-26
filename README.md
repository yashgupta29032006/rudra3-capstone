# Rudra 3.0 — Multi-Agent Personal Assistant (Capstone)

Rudra 3.0 is a multi-agent, multi-modal personal assistant designed and refactored as a competition-ready submission for the Kaggle × Google Agents Intensive Capstone.  
It demonstrates multi-agent orchestration, vision-enabled automation, long-running monitoring, sessions & memory, observability, and optional identity workflows — all structured for clarity, reproducibility, and ethical use.

---

## Key Features (mapped to rubric)
- **Multi-agent system**: `RouterAgent`, `VisionAgent`, `AutomationAgent`, `MemoryAgent`, `MonitorAgent`, `IdentityAgent`.
- **Tools / MCP wrappers**: `Tools` (screenshot, click, open_app, imagesnap_save) provide deterministic OS-level actions.
- **Long-running operations**: `MonitorAgent` runs continuously to detect the frontmost app and trigger periodic checks (loop agent).
- **Sessions & Memory**: `MemoryAgent` persists chat history and learned behaviors; includes compaction.
- **Observability**: `Logger` records structured logs and basic metrics (commands_executed, vision_calls, errors).
- **Agent evaluation**: Confidence/trace ids included in logs; agent decisions recorded for offline evaluation.
- **Optional identity module**: Face capture is opt-in and disabled by default for privacy compliance.

Bonus features available in repo:
- **Gemini-compatible stubs**: Integrate Gemini or other LLM/vision providers via env var.
- **CLI demo** and scaffolding for Telegram integration (disabled until credentials are configured).

---

## Requirements
Install Python 3.10+ and then:

```bash
pip install -r requirements.txt
