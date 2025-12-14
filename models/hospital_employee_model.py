from models.person_model import Person
from abc import ABC, abstractmethod
from enum import Enum, auto


class Department(Enum):
    DOCTOR = auto()
    NURSE = auto()


class HospitalEmployee(Person, ABC):
    def __init__(self, full_name, age, gender, work_id, department):
        super().__init__(full_name, age, gender)
        if isinstance(work_id, int):
            self._work_id = work_id
        else:
            raise TypeError("Must be an integer.")
        if isinstance(department, Department):
            self._department = department
        else:
            raise TypeError("Department must be an instance of Department enum")

    def generate_unique_identifier(self):
        return f'{self._work_id}'

    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def perform_duty(self):
        pass

    @abstractmethod
    def assign_task(self, new_task):
        pass

    def display_department(self):
        if self._department == Department.DOCTOR:
            return 'Doctor'
        elif self._department == Department.NURSE:
            return 'Nurse'

    @property
    def department(self):
        return self._department

    @property
    def work_id(self):
        return self._work_id

    @work_id.setter
    def work_id(self, new_id):
        if isinstance(new_id, int):
            self._work_id = new_id
        else:
            raise TypeError("Must be an integer")
