from models.patient_model import Patient


class Task:
    def __init__(self, description, patient, priority):
        self._description = description
        if isinstance(patient, Patient):
            self._patient = patient
        else:
            raise TypeError("Must be a Patient instance.")
        if isinstance(priority, int):
            self._priority = priority
        else:
            raise TypeError("Must be an integer.")
        self._is_completed = False

    def mark_completed(self):
        self._is_completed = True

    @property
    def description(self):
        return self._description

    @property
    def patient(self):
        return self._patient

    @property
    def priority(self):
        return self._priority
