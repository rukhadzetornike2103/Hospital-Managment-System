from models.patient_model import Patient, AdmissionStatus, Condition
from models.room_model import Room


class InPatient(Patient):
    def __init__(self, full_name, age, gender, contact_info, personal_number, insurance, condition, room):
        super().__init__(full_name, age, gender, contact_info, personal_number, insurance, condition)
        if isinstance(room, Room):
            self._room = room
        else:
            raise TypeError("Must be an instance of Room")

    def generate_unique_identifier(self):
        initials = ''.join(word[0].upper() for word in self._full_name.split())
        return f'IP_{initials}_{self._age}'

    def display_info(self):
        print("Name: ", self._full_name)
        print("Age:", self._age)
        print("Medical History:", self.display_medical_history())
        print("Condition:", self.display_condition())
        print("Admission status:", self.display_admission_status())
        print("Room: ", self._room.__str__())

    def discharge(self):
        self.change_admission_status(AdmissionStatus.DISCHARGED)

    def provide_treatment_details(self, entry):
        self._prescriptions.append(entry)

    def admit(self):
        self.change_admission_status(AdmissionStatus.ADMITTED)

    @property
    def room(self):
        return self._room

    @room.setter
    def room(self, new_r):
        self._room = new_r if isinstance(new_r, Room) else TypeError("Must be an instance of Room")

    def __repr__(self):
        return f'Inpatient class.'