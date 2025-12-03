# ...existing code...
from statistics import mean
import sys
from pathlib import Path
import re

# adiciona o diretório pai (src) ao path para importar data_store
sys.path.insert(0, str(Path(__file__).parent.parent))
import data_store

class PatientController:
    def __init__(self):
        self.patients = data_store.patients

    def _normalize_cpf(self, cpf_raw: str) -> str:
        return re.sub(r"\D", "", (cpf_raw or ""))

    def _format_cpf(self, cpf_digits: str) -> str:
        if len(cpf_digits) == 11:
            return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"
        return cpf_digits

    def _cpf_exists(self, cpf_digits: str) -> bool:
        return any(self._normalize_cpf(p.get("cpf", "")) == cpf_digits for p in self.patients)

    def _valid_cpf_digits(self, cpf: str) -> bool:
        """Valida dígitos verificadores do CPF (assume cpf contém apenas dígitos)."""
        if not cpf or len(cpf) != 11:
            return False
        # rejeita sequências iguais (ex: 00000000000)
        if cpf == cpf[0] * 11:
            return False
        nums = [int(ch) for ch in cpf]
        # primeiro dígito verificador
        s = sum(nums[i] * (10 - i) for i in range(9))
        r = s % 11
        d1 = 0 if r < 2 else 11 - r
        if nums[9] != d1:
            return False
        # segundo dígito verificador
        s = sum(nums[i] * (11 - i) for i in range(10))
        r = s % 11
        d2 = 0 if r < 2 else 11 - r
        if nums[10] != d2:
            return False
        return True

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

        cpf_input = input("CPF (somente números ou formatado): ").strip()
        cpf_digits = self._normalize_cpf(cpf_input)
        if len(cpf_digits) != 11:
            print("CPF inválido. Deve conter 11 dígitos.")
            return
        if not self._valid_cpf_digits(cpf_digits):
            print("CPF inválido (dígitos verificadores não conferem).")
            return
        if self._cpf_exists(cpf_digits):
            print("CPF já cadastrado.")
            return

        paciente = {"nome": nome, "idade": idade, "telefone": telefone, "cpf": cpf_digits}
        self.patients.append(paciente)
        data_store.save()
        print("Paciente cadastrado com sucesso!")

    def search_patient(self):
        termo = input("Nome ou CPF para busca: ").strip()
        termo_digits = self._normalize_cpf(termo)
        encontrados = []
        for p in self.patients:
            nome = p.get("nome", "").lower()
            cpf = self._normalize_cpf(p.get("cpf", ""))
            if termo_digits and termo_digits in cpf:
                encontrados.append(p)
            elif termo and termo.lower() in nome:
                encontrados.append(p)

        if not encontrados:
            print("Nenhum paciente encontrado.")
            return []

        print("Resultados da busca:")
        for i, p in enumerate(encontrados, 1):
            cpf_display = self._format_cpf(p.get("cpf", ""))
            print(f"{i}. {p.get('nome')} — {p.get('idade')} — {p.get('telefone')} — CPF: {cpf_display}")
        return encontrados

    def list_patients(self):
        if not self.patients:
            print("Nenhum paciente cadastrado.")
            return []
        print("Lista de pacientes:")
        for i, p in enumerate(self.patients, 1):
            cpf_display = self._format_cpf(p.get("cpf", ""))
            print(f"{i}. {p.get('nome')} — {p.get('idade')} — {p.get('telefone')} — CPF: {cpf_display}")
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
        print(f"Mais novo: {mais_novo['nome']} ({mais_novo['idade']} anos) — CPF: {self._format_cpf(mais_novo.get('cpf',''))}")
        print(f"Mais velho: {mais_velho['nome']} ({mais_velho['idade']} anos) — CPF: {self._format_cpf(mais_velho.get('cpf',''))}")
# ...existing code...