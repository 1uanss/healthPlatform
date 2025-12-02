import sys
from pathlib import Path

# adiciona o diretório pai (src) ao path para importar data_store
sys.path.insert(0, str(Path(__file__).parent.parent))
import data_store

class QueueController:
    def __init__(self):
        self.queue = data_store.queue
        self.patients = data_store.patients

    def _patient_name(self, patient):
        if isinstance(patient, dict):
            return patient.get("nome") or patient.get("name") or "Desconhecido"
        return str(patient)

    def add_patient_to_queue(self, patient):
        self.queue.append(patient)
        data_store.save()
        print(f"Paciente {self._patient_name(patient)} adicionado à fila.")

    def remove_patient_from_queue(self):
        if self.queue:
            patient = self.queue.pop(0)
            data_store.save()
            print(f"Paciente {self._patient_name(patient)} está sendo atendido.")
            return patient
        else:
            print("Nenhum paciente na fila.")
            return None

    def get_queue(self):
        return self.queue

    def queue_length(self):
        return len(self.queue)

    def attend_next_patient(self):
        while True:
            print("\n--- FILA DE ATENDIMENTO ---")
            if not self.queue:
                print("Fila vazia.")
            else:
                for i, p in enumerate(self.queue, 1):
                    nome = self._patient_name(p)
                    idade = p.get("idade", "?") if isinstance(p, dict) else "?"
                    print(f"{i}. {nome} — {idade} anos")

            print("\nOpções:")
            print("1. Adicionar paciente à fila")
            print("2. Atender próximo")
            print("3. Mostrar fila")
            print("4. Voltar ao menu principal")
            opc = input("Escolha: ").strip()

            if opc == "1":
                if not self.patients:
                    print("Nenhum paciente cadastrado. Cadastre antes.")
                    continue
                print("Pacientes cadastrados:")
                for idx, p in enumerate(self.patients, 1):
                    print(f"{idx}. {p.get('nome')} — {p.get('idade', '?')} anos")
                try:
                    sel = int(input("Número do paciente para adicionar: ").strip())
                    if sel < 1 or sel > len(self.patients):
                        raise ValueError
                except ValueError:
                    print("Seleção inválida.")
                    continue
                self.add_patient_to_queue(self.patients[sel - 1])
            elif opc == "2":
                self.remove_patient_from_queue()
            elif opc == "3":
                if not self.queue:
                    print("Fila vazia.")
                else:
                    print("Fila atual:")
                    for i, p in enumerate(self.queue, 1):
                        print(f"{i}. {self._patient_name(p)}")
            elif opc == "4":
                break
            else:
                print("Opção inválida.")