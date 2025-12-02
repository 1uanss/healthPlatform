def register_patient(patients, name, age, phone):
    if not validate_input(name, age, phone):
        return "Invalid input data."
    
    patient_id = len(patients) + 1
    patient = {
        'id': patient_id,
        'name': name,
        'age': age,
        'phone': phone
    }
    patients.append(patient)
    return f"Patient {name} registered successfully."

def validate_input(name, age, phone):
    if not name or not isinstance(name, str):
        return False
    if not isinstance(age, int) or age <= 0:
        return False
    if not phone or not isinstance(phone, str):
        return False
    return True