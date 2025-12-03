import sys
from pathlib import Path
from datetime import datetime
import uuid

sys.path.insert(0, str(Path(__file__).parent.parent))
import data_store

class AttendanceController:
    def __init__(self):
        self.history = data_store.appointments_history
        self.patients = data_store.patients
        self.doctors = data_store.doctors
        self.appointments = data_store.appointments

    def _find_patient_by_cpf(self, cpf_digits):
        for p in self.patients:
            if ''.join(filter(str.isdigit, p.get("cpf", ""))) == cpf_digits:
                return p
        return None

    def _format_cpf(self, cpf_digits: str) -> str:
        if len(cpf_digits) == 11:
            return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"
        return cpf_digits

    def register_attendance(self):
        """Registra um novo atendimento (consulta realizada)."""
        cpf_input = input("CPF do paciente (números ou formatado): ").strip()
        cpf_digits = ''.join(filter(str.isdigit, cpf_input))
        if len(cpf_digits) != 11:
            print("CPF inválido (11 dígitos necessários).")
            return

        patient = self._find_patient_by_cpf(cpf_digits)
        if not patient:
            print("Paciente não encontrado.")
            return

        # escolher médico
        print("Médicos disponíveis:")
        for d in self.doctors:
            print(f"{d['id']}. {d['nome']} — {d['especialidade']}")
        try:
            doc_sel = int(input("ID do médico responsável: ").strip())
            doctor = next((d for d in self.doctors if d["id"] == doc_sel), None)
            if not doctor:
                print("Médico não encontrado.")
                return
        except ValueError:
            print("ID inválido.")
            return

        diagnosis = input("Diagnóstico: ").strip()
        treatment = input("Tratamento prescrito: ").strip()
        notes = input("Observações adicionais: ").strip()

        attendance = {
            "id": str(uuid.uuid4())[:8],
            "cpf": cpf_digits,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "doctor": doctor["nome"],
            "diagnosis": diagnosis,
            "treatment": treatment,
            "notes": notes
        }
        self.history.append(attendance)
        data_store.save()
        print(f"Atendimento registrado com sucesso! ID: {attendance['id']}")

    def view_patient_history(self):
        """Exibe histórico de evolução de um paciente."""
        cpf_input = input("CPF do paciente: ").strip()
        cpf_digits = ''.join(filter(str.isdigit, cpf_input))
        if len(cpf_digits) != 11:
            print("CPF inválido.")
            return

        patient = self._find_patient_by_cpf(cpf_digits)
        if not patient:
            print("Paciente não encontrado.")
            return

        # filtrar histórico do paciente
        patient_history = [a for a in self.history if a["cpf"] == cpf_digits]
        if not patient_history:
            print(f"Nenhum atendimento registrado para {patient['nome']}.")
            return

        print(f"\n--- HISTÓRICO DE {patient['nome']} ({self._format_cpf(cpf_digits)}) ---")
        for i, att in enumerate(patient_history, 1):
            print(f"\n{i}. Data: {att['date']}")
            print(f"   Médico: {att['doctor']}")
            print(f"   Diagnóstico: {att['diagnosis']}")
            print(f"   Tratamento: {att['treatment']}")
            print(f"   Observações: {att['notes']}")

    def list_all_attendance(self):
        """Lista todos os atendimentos registrados."""
        if not self.history:
            print("Nenhum atendimento registrado.")
            return []

        print("\n--- TODOS OS ATENDIMENTOS ---")
        for att in self.history:
            patient = self._find_patient_by_cpf(att["cpf"])
            name = patient.get("nome") if patient else att["cpf"]
            print(f"ID: {att['id']} | {att['date']} | {name} | {att['doctor']} | Diagnóstico: {att['diagnosis']}")
        return self.history

    def edit_attendance(self):
        """Edita um atendimento registrado."""
        aid = input("ID do atendimento a editar: ").strip()
        for att in self.history:
            if att["id"] == aid:
                print(f"Editando atendimento {aid}:")
                print(f"Diagnóstico atual: {att['diagnosis']}")
                new_diagnosis = input("Novo diagnóstico (Enter para manter): ").strip()
                if new_diagnosis:
                    att["diagnosis"] = new_diagnosis

                print(f"Tratamento atual: {att['treatment']}")
                new_treatment = input("Novo tratamento (Enter para manter): ").strip()
                if new_treatment:
                    att["treatment"] = new_treatment

                print(f"Observações atuais: {att['notes']}")
                new_notes = input("Novas observações (Enter para manter): ").strip()
                if new_notes:
                    att["notes"] = new_notes

                data_store.save()
                print("Atendimento atualizado com sucesso!")
                return
        print("Atendimento não encontrado.")

    def manage_menu(self):
        while True:
            print("\n--- GESTÃO DE ATENDIMENTOS ---")
            print("1. Registrar novo atendimento")
            print("2. Ver histórico de paciente")
            print("3. Listar todos os atendimentos")
            print("4. Editar atendimento")
            print("5. Voltar")
            opc = input("Escolha: ").strip()
            if opc == "1":
                self.register_attendance()
            elif opc == "2":
                self.view_patient_history()
            elif opc == "3":
                self.list_all_attendance()
            elif opc == "4":
                self.edit_attendance()
            elif opc == "5":
                break
            else:
                print("Opção inválida.")