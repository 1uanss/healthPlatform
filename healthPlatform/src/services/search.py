def search_patient_by_name(patients, name):
    """Search for a patient by name in the list of patients."""
    return [patient for patient in patients if patient.name.lower() == name.lower()]

def search_patient_by_age(patients, age):
    """Search for patients by age in the list of patients."""
    return [patient for patient in patients if patient.age == age]

def search_patient_by_phone(patients, phone):
    """Search for a patient by phone number in the list of patients."""
    return [patient for patient in patients if patient.phone == phone]