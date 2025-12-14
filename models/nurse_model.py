from models.hospital_employee_model import HospitalEmployee
from datetime import datetime


class Nurse(HospitalEmployee):
    def __init__(self, full_name, age, gender, work_id, department):
        super().__init__(full_name, age, gender, work_id, department)
        self._upcoming_shifts = []
        self._completed_shifts = []
        self._assigned_tasks = []
        self._completed_tasks = []

    def generate_unique_identifier(self):
        return f'N_{self.work_id}'

    def display_info(self):
        print("Name:", self._full_name)
        print("Age:", self._age)
        print("Department:", self.display_department())
        print("ID: ", self.generate_unique_identifier())

    def perform_duty(self):
        sorted_tasks = sorted(self._assigned_tasks, key=lambda x: x.priority)
        highest_priority_task = sorted_tasks[0]
        highest_priority_task.mark_completed()
        self._completed_tasks.append(highest_priority_task)
        self._assigned_tasks.remove(highest_priority_task)

    def assign_task(self, new_task):
        self._assigned_tasks.append(new_task)

    def display_assigned_tasks(self):
        print("Assigned tasks:\n")
        for task in self._assigned_tasks:
            print("Description: ", task.description)
            print("Patient:", task.patient.display_info())

    def add_shift(self, shift):
        self._upcoming_shifts.append(shift)

    def start_shift(self):
        if not self._upcoming_shifts:
            print("No upcoming shift to start.")
            return None
        start_date_time = datetime.now()
        shift = self._upcoming_shifts.pop(0)  # Pop the first shift from the list
        shift._start_date_time = start_date_time
        print(f"Nurse {self._full_name} started shift at {start_date_time}.")
        return shift

    def end_shift(self):
        if not self._upcoming_shifts:
            print("No active shift to end.")
            return
        end_date_time = datetime.now()
        shift = self._upcoming_shifts.pop()
        shift._end_date_time = end_date_time
        self._completed_shifts.append(shift)
        print(f"Nurse {self._full_name} ended shift at {end_date_time}.")

    @property
    def assigned_tasks(self):
        return self._assigned_tasks

    @property
    def completed_tasks(self):
        return self._completed_tasks
