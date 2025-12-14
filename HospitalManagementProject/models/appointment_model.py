from models.patient_model import Patient
from models.doctor_model import Doctor
from enum import Enum
import datetime


class AppointmentType(Enum):
    SURGERY = "Surgery"
    CONSULTATION = "Consultation"
    VISIT = "Visit"
    PROCEDURE = "Procedure"


class Appointment:
    _appointment_id_counter = 0

    def __init__(self, description, date_time, appointment_type, patient):
        self._appointment_id = self.generate_appointment_id()
        self._description = description
        if isinstance(patient, Patient):
            self._patient = patient
        else:
            raise TypeError("Must be a Patient instance.")
        if isinstance(appointment_type, AppointmentType):
            self._appointment_type = appointment_type
        else:
            raise TypeError("Must be a valid appointment type.")
        self._notes = []
        self._doctor = None
        self._is_completed = False
        self._date_time = date_time

    @classmethod
    def generate_appointment_id(cls):
        cls._appointment_id_counter += 1
        return cls._appointment_id_counter

    def add_doctor(self, doctor):
        if isinstance(doctor, Doctor):
            self._doctor = doctor
        else:
            raise TypeError("Doctor must be an instance of doctor.")

    def print_details(self):
        print("Description: ", self._description)
        print("Appointment type: ", self.display_type())
        print(f'Patient name: {self.patient.full_name} | ID: {self.patient.generate_unique_identifier()}')
        print(f'Doctor name: {self.doctor.full_name} | ID: {self.doctor.generate_unique_identifier()}')
        print("Notes:\n", self.display_notes())

    def mark_completed(self):
        self._is_completed = True

    def add_note(self, note):
        self._notes.append(note)

    def display_notes(self):
        for note in self._notes:
            print(note)

    def display_type(self):
        if self._appointment_type == AppointmentType.CONSULTATION:
            return 'Consultation'
        elif self._appointment_type == AppointmentType.VISIT:
            return 'Visit'
        elif self._appointment_type == AppointmentType.SURGERY:
            return 'Surgery'
        elif self._appointment_type == AppointmentType.PROCEDURE:
            return 'Procedure'

    @property
    def description(self):
        return self._description

    @property
    def date_time(self):
        return self._date_time

    @property
    def patient(self):
        return self._patient

    @property
    def doctor(self):
        return self._doctor

    @property
    def appointment_type(self):
        return self._appointment_type

    @property
    def notes(self):
        return self._notes

    @property
    def appointment_id(self):
        return self._appointment_id

    @property
    def is_completed(self):
        return self._is_completed
