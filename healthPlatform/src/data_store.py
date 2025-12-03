import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data.json"

# estruturas em memória (mutáveis, usadas por controllers)
patients = []
queue = []
appointments = []
appointments_history = []  # lista de dicts: {"id", "cpf", "date", "doctor", "diagnosis", "treatment", "notes"}
doctors = [
    {"id": 1, "nome": "Dr. Carlos Silva", "especialidade": "Clínico Geral"},
    {"id": 2, "nome": "Dra. Ana Pereira", "especialidade": "Pediatria"},
]

def load():
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            patients.clear()
            patients.extend(data.get("patients", []))
            queue.clear()
            queue.extend(data.get("queue", []))
            appointments.clear()
            appointments.extend(data.get("appointments", []))
            appointments_history.clear()
            appointments_history.extend(data.get("appointments_history", []))
            doctors_data = data.get("doctors")
            if doctors_data:
                doctors.clear()
                doctors.extend(doctors_data)
    except Exception:
        patients.clear()
        queue.clear()
        appointments.clear()
        appointments_history.clear()

def save():
    try:
        DATA_FILE.write_text(
            json.dumps(
                {
                    "patients": patients,
                    "queue": queue,
                    "appointments": appointments,
                    "appointments_history": appointments_history,
                    "doctors": doctors
                },
                ensure_ascii=False, indent=2
            ),
            encoding="utf-8"
        )
    except Exception:
        pass

# carrega automaticamente ao importar
load()