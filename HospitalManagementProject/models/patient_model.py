from abc import ABC, abstractmethod
from models.person_model import Person
from enum import Enum, auto


class AdmissionStatus(Enum):
    ADMITTED = "Admitted"
    DISCHARGED = "Discharged"
    PENDING = "Observation"


class Condition(Enum):
    STABLE = "Stable"
    CRITICAL = "Critical"
    OBSERVATION = "Observation"
    RECOVERING = "Recovering"
    UNDER_TREATMENT = "Under treatment"
    DECEASED = "Deceased"
    AWAITING_SURGERY = "Awaiting surgery"
    QUARANTINE = "Quarantine"
    PALLIATIVE_CARE = "Palliative care"
    UNKNOWN = "Unknown"
    REFUSED = "Refused"
    TRANSFERRED = "Transferred"


class Patient(Person, ABC):
    def __init__(self, full_name, age, gender, contact_info, personal_number, insurance, condition):
        super().__init__(full_name, age, gender)
        self._contact_info = contact_info
        self._personal_number = personal_number
        self._insurance = insurance
        if isinstance(condition, Condition):
            self._condition = condition
        else:
            raise ValueError("Condition must be an instance of Condition enum. ")
        self._cards = []
        self._balance = 0.0
        self._prescriptions = []
        self._medical_history = []
        self._admission_status = AdmissionStatus.PENDING

    @abstractmethod
    def discharge(self):
        pass

    @abstractmethod
    def provide_treatment_details(self, entry):
        pass

    @abstractmethod
    def admit(self):
        pass

    @abstractmethod
    def generate_unique_identifier(self):
        pass

    def display_info(self):
        print("Name: ", self._full_name)
        print("Age:", self._age)
        print("Medical History:", self.display_medical_history())
        print("Condition: ", self.display_condition())
        print("Admission status: ", self.display_admission_status())

    def display_admission_status(self):
        if self._admission_status == AdmissionStatus.ADMITTED:
            return 'Admitted'
        elif self._admission_status == AdmissionStatus.DISCHARGED:
            return 'Discharged'
        elif self._admission_status == AdmissionStatus.PENDING:
            return 'Pending'
        elif self._admission_status == AdmissionStatus.REFUSED:
            return 'Refused'
        elif self._admission_status == AdmissionStatus.TRANSFERRED:
            return 'Transferred'

    def display_condition(self):
        if self._condition == Condition.STABLE:
            return 'Stable'
        elif self._condition == Condition.CRITICAL:
            return 'Critical'
        elif self._condition == Condition.DECEASED:
            return 'Deceased'
        elif self._condition == Condition.AWAITING_SURGERY:
            return 'Awaiting surgery'
        elif self._condition == Condition.OBSERVATION:
            return 'Observation'
        elif self._condition == Condition.QUARANTINE:
            return 'Quarantine'
        elif self._condition == Condition.UNDER_TREATMENT:
            return 'Under treatment'
        elif self._condition == Condition.RECOVERING:
            return 'Recovering'
        elif self._condition == Condition.PALLIATIVE_CARE:
            return 'Palliative care'
        elif self._condition == Condition.UNKNOWN:
            return 'Unknown'

    def display_prescriptions(self):
        for prescription in self._prescriptions:
            print(prescription)

    def deposit(self, amount):
        self._balance += amount

    def charge(self, amount):
        self._balance -= amount

    def clear_balance(self):
        self._balance = 0

    def add_payment_method(self, card_info):
        self._cards.append(card_info)

    def add_medical_history(self, entry):
        self._medical_history.append(entry)

    def display_medical_history(self):
        for entry in self._medical_history:
            print(entry)

    def change_admission_status(self, new_s):
        if isinstance(new_s, AdmissionStatus):
            self._admission_status = new_s
        else:
            raise ValueError("Admission status must be an instance of AdmissionStatus enum. ")

    def add_prescription(self, entry):
        self._prescriptions.append(entry)

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, new_inf):
        self._contact_info = new_inf

    @property
    def personal_number(self):
        return self._personal_number

    @personal_number.setter
    def personal_number(self, new_n):
        if isinstance(new_n, str):
            self._personal_number = new_n
        else:
            raise TypeError(f'{type(new_n).__name__} type not supported. Should be of {type(str).__name__} type.')

    @property
    def insurance(self):
        return self._insurance

    @insurance.setter
    def insurance(self, new_ins):
        if isinstance(new_ins, str):
            self._insurance = new_ins
        else:
            raise TypeError(f'{type(new_ins).__name__} type not supported. Should be of {type(str).__name__} type.')

    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, new_c):
        if isinstance(new_c, Condition):
            self._condition = new_c
        else:
            raise ValueError("Condition must be an instance of Condition enum. ")

    @property
    def medical_history(self):
        return self._medical_history

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_b):
        if isinstance(new_b, (int, float)):
            self._balance = float(new_b)
        else:
            raise TypeError("Must be integer or float.")

    @property
    def prescriptions(self):
        return self._prescriptions

    @property
    def cards(self):
        return self._cards

    @property
    def admission_status(self):
        return self._admission_status
