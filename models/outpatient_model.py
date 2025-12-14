import models.patient_model
from models.patient_model import Patient, Condition, AdmissionStatus


class OutPatient(Patient):
    def __init__(self, full_name, age, gender, contact_info, personal_number, insurance, condition):
        super().__init__(full_name, age, gender, contact_info, personal_number, insurance, condition)

    def admit(self):
        self.change_admission_status(AdmissionStatus.ADMITTED)

    def discharge(self):
        self.change_admission_status(AdmissionStatus.DISCHARGED)

    def provide_treatment_details(self, entry):
        self._prescriptions.append(entry)

    def generate_unique_identifier(self):
        initials = ''.join(word[0].upper() for word in self._full_name.split())
        return f'OP_{initials}_{self._age}'

    def display_info(self):
        print("Name: ", self._full_name)
        print("Age:", self._age)
        print("Medical History:", self.display_medical_history())
        print("Condition:", self.display_condition())
        print("Admission status:", self.display_admission_status())

    def __repr__(self):
        return f'Outpatient class.'