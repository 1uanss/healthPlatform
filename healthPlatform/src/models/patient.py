class Patient:
    def __init__(self, name, age, phone_number):
        self.name = name
        self.age = age
        self.phone_number = phone_number

    def __repr__(self):
        return f"Patient(name={self.name}, age={self.age}, phone_number={self.phone_number})"