import sys
from pathlib import Path
from datetime import datetime, timedelta
import uuid

# garantir import do data_store quando executado a partir de src
sys.path.insert(0, str(Path(__file__).parent.parent))
import data_store

class AppointmentController:
    def __init__(self):
        self.appointments = data_store.appointments
        self.patients = data_store.patients
        self.doctors = data_store.doctors

    def _find_patient_by_cpf(self, cpf_digits):
        for p in self.patients:
            if ''.join(filter(str.isdigit, p.get("cpf", ""))) == cpf_digits:
                return p
        return None

    def _generate_slots(self, date_str, start="09:00", end="17:00", slot_minutes=30):
        """Retorna lista de strings 'HH:MM' dos slots entre start e end."""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start_dt = datetime.combine(date.date(), datetime.strptime(start, "%H:%M").time())
        end_dt = datetime.combine(date.date(), datetime.strptime(end, "%H:%M").time())
        slots = []
        cur = start_dt
        while cur < end_dt:
            slots.append(cur.strftime("%H:%M"))
            cur += timedelta(minutes=slot_minutes)
        return slots

    def available_slots(self, date_str):
        all_slots = self._generate_slots(date_str)
        occupied = { (a["date"], a["time"]) for a in self.appointments if a["date"] == date_str and a["status"] != "cancelado" }
        return [s for s in all_slots if (date_str, s) not in occupied]

    def list_appointments(self):
        if not self.appointments:
            print("Nenhum agendamento.")
            return []
        print("\n--- LISTA DE AGENDAMENTOS ---")
        for a in self.appointments:
            patient = self._find_patient_by_cpf(''.join(filter(str.isdigit, a.get("cpf",""))))
            name = patient.get("nome") if patient else a.get("cpf")
            doctor = next((d["nome"] for d in self.doctors if d["id"] == a.get("doctor")), "Sem médico")
            print(f"ID: {a['id']} | {a['tipo'].upper()} | {a['date']} {a['time']} | {name} | {doctor} | {a['status'].upper()}")
        return self.appointments

    def schedule_appointment(self):
        cpf_input = input("CPF do paciente (números ou formatado): ").strip()
        cpf_digits = ''.join(filter(str.isdigit, cpf_input))
        if len(cpf_digits) != 11:
            print("CPF inválido (11 dígitos necessários).")
            return
        patient = self._find_patient_by_cpf(cpf_digits)
        if not patient:
            print("Paciente não encontrado. Cadastre antes.")
            return

        tipo = input("Tipo (consulta/exame): ").strip().lower()
        if tipo not in ("consulta", "exame"):
            print("Tipo inválido.")
            return

        date_str = input("Data (AAAA-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            print("Data inválida.")
            return

        slots = self.available_slots(date_str)
        if not slots:
            print("Nenhum slot disponível nessa data.")
            return

        print("Slots disponíveis:")
        for i, s in enumerate(slots, 1):
            print(f"{i}. {s}")
        try:
            sel = int(input("Escolha o número do slot: ").strip())
            if sel < 1 or sel > len(slots):
                raise ValueError
        except ValueError:
            print("Seleção inválida.")
            return
        time_selected = slots[sel - 1]

        # escolha de médico
        print("Médicos disponíveis:")
        for d in self.doctors:
            print(f"{d['id']}. {d['nome']} — {d['especialidade']}")
        try:
            doc_sel = int(input("Escolha o id do médico (ou 0 para nenhum): ").strip())
        except ValueError:
            print("Opção inválida.")
            return
        doctor_id = doc_sel if any(d["id"] == doc_sel for d in self.doctors) else None

        appt = {
            "id": str(uuid.uuid4())[:8],
            "cpf": cpf_digits,
            "tipo": tipo,
            "date": date_str,
            "time": time_selected,
            "doctor": doctor_id,
            "status": "agendado"
        }
        self.appointments.append(appt)
        data_store.save()
        print(f"Agendamento criado: {appt['id']} — {date_str} {time_selected}")

    def cancel_appointment(self):
        self.list_appointments()
        aid = input("ID do agendamento a cancelar: ").strip()
        for a in self.appointments:
            if a["id"] == aid:
                a["status"] = "cancelado"
                data_store.save()
                print("Agendamento cancelado.")
                return
        print("Agendamento não encontrado.")

    def manage_menu(self):
        while True:
            print("\n--- GESTÃO DE AGENDAMENTOS ---")
            print("1. Agendar consulta/exame")
            print("2. Listar agendamentos")
            print("3. Ver slots disponíveis por data")
            print("4. Cancelar agendamento")
            print("5. Voltar")
            opc = input("Escolha: ").strip()
            if opc == "1":
                self.schedule_appointment()
            elif opc == "2":
                self.list_appointments()
            elif opc == "3":
                date_str = input("Data (AAAA-MM-DD): ").strip()
                try:
                    slots = self.available_slots(date_str)
                    if not slots:
                        print("Nenhum slot disponível nessa data.")
                    else:
                        print(f"Slots disponíveis para {date_str}:")
                        for s in slots:
                            print(f"- {s}")
                except Exception:
                    print("Data inválida.")
            elif opc == "4":
                self.cancel_appointment()
            elif opc == "5":
                break
            else:
                print("Opção inválida.")

