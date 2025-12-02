import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data.json"

# estruturas em memória (mutáveis, usadas por controllers)
patients = []
queue = []

def load():
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            patients.clear()
            patients.extend(data.get("patients", []))
            queue.clear()
            queue.extend(data.get("queue", []))
    except Exception:
        patients.clear()
        queue.clear()

def save():
    try:
        DATA_FILE.write_text(
            json.dumps({"patients": patients, "queue": queue}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception:
        pass

# carrega automaticamente ao importar
load()