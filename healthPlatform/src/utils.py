def validate_name(name):
    if not isinstance(name, str) or len(name) == 0:
        raise ValueError("Name must be a non-empty string.")
    return name

def validate_age(age):
    if not isinstance(age, int) or age <= 0:
        raise ValueError("Age must be a positive integer.")
    return age

def validate_phone(phone):
    if not isinstance(phone, str) or len(phone) < 10:
        raise ValueError("Phone number must be a string with at least 10 digits.")
    return phone

def handle_error(error):
    print(f"Error: {error}")