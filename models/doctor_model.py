from models.hospital_employee_model import HospitalEmployee
from models.patient_model import Patient


class Doctor(HospitalEmployee):
    def __init__(self, full_name, age, gender, work_id, department, specialization):
        super().__init__(full_name, age, gender, work_id, department)
        self._specialization = specialization
        self._upcoming_appointments = []

    def generate_unique_identifier(self):
        return f'D_{self.work_id}'

    def display_info(self):
        print("Name:", self._full_name)
        print("Age:", self._age)
        print("Department:", self.display_department())
        print("ID: ", self.generate_unique_identifier())

    def perform_duty(self):
        if self._upcoming_appointments:
            # Pop the last appointment from the list
            appointment = self._upcoming_appointments[-1]
            return appointment
        else:
            # If no upcoming appointments, return None
            return None

    @staticmethod
    def prescribe(patient, entry):
        patient.add_prescription(entry)

    def assign_task(self, new_task):
        self._upcoming_appointments.append(new_task)

    def display_appointments(self):
        print("Upcoming appointments:\n")
        for appointment in self._upcoming_appointments:
            print(appointment)

    @property
    def specialization(self):
        return self._specialization

    @property
    def appointments(self):
        return self._upcoming_appointments
