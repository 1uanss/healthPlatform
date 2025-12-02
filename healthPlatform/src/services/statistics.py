def calculate_total_patients(patients):
    return len(patients)

def calculate_average_age(patients):
    if not patients:
        return 0
    total_age = sum(patient.age for patient in patients)
    return total_age / len(patients)

def find_youngest_patient(patients):
    if not patients:
        return None
    return min(patients, key=lambda patient: patient.age)

def find_oldest_patient(patients):
    if not patients:
        return None
    return max(patients, key=lambda patient: patient.age)