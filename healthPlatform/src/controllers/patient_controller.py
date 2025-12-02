from statistics import mean
import sys
from pathlib import Path

# adiciona o diretório pai (src) ao path para importar data_store
sys.path.insert(0, str(Path(__file__).parent.parent))
import data_store

class PatientController:
    def __init__(self):
        self.patients = data_store.patients

    def register_patient(self):
        nome = input("Nome do paciente: ").strip()
        if not nome:
            print("Nome inválido.")
            return
        try:
            idade = int(input("Idade: ").strip())
            if idade < 0:
                raise ValueError
        except ValueError:
            print("Idade inválida.")
            return
        telefone = input("Telefone: ").strip()
        paciente = {"nome": nome, "idade": idade, "telefone": telefone}
        self.patients.append(paciente)
        data_store.save()
        print("Paciente cadastrado com sucesso!")

    def search_patient(self):
        termo = input("Nome para busca: ").strip().lower()
        encontrados = [p for p in self.patients if termo in p.get("nome", "").lower()]
        if not encontrados:
            print("Nenhum paciente encontrado.")
            return []
        print("Resultados da busca:")
        for i, p in enumerate(encontrados, 1):
            print(f"{i}. {p.get('nome')} — {p.get('idade')} — {p.get('telefone')}")
        return encontrados

    def list_patients(self):
        if not self.patients:
            print("Nenhum paciente cadastrado.")
            return []
        print("Lista de pacientes:")
        for i, p in enumerate(self.patients, 1):
            print(f"{i}. {p.get('nome')} — {p.get('idade')} — {p.get('telefone')}")
        return self.patients

    def view_statistics(self):
        if not self.patients:
            print("Nenhum paciente cadastrado.")
            return
        total = len(self.patients)
        media = mean(p["idade"] for p in self.patients)
        mais_novo = min(self.patients, key=lambda p: p["idade"])
        mais_velho = max(self.patients, key=lambda p: p["idade"])
        print(f"Total de pacientes: {total}")
        print(f"Idade média: {media:.1f}")
        print(f"Mais novo: {mais_novo['nome']} ({mais_novo['idade']} anos)")
        print(f"Mais velho: {mais_velho['nome']} ({mais_velho['idade']} anos)")