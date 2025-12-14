from models.inpatient_model import InPatient
from models.patient_model import Condition
from models.room_model import Room
from models.doctor_model import Doctor
from models.hospital_employee_model import Department
from log_config import setup_logging
from controllers.database_controller import DatabaseController
from models.appointment_model import Appointment, AppointmentType
from datetime import datetime, time
from controllers.nurse_controller import NurseController
from models.nurse_model import Nurse
from models.nurse_shift_model import Shift, ShiftType
from models.task_model import Task

logger = setup_logging()
db_controller = DatabaseController()


def main():
    room = Room("19191", Room.RoomType.SINGLE, 50)
    inpatient = InPatient("Vlad Mandache", 21, 'Male', "vlad.gfx@yahoo.com", "200189888", "AETNA", Condition.STABLE, room)
    appointment = Appointment("Surgery", datetime.now(), AppointmentType.SURGERY, inpatient)
    doctor = Doctor("TEST", 21, 'MALE', 22292, Department.DOCTOR, "cafridoloy")
    nurse = Nurse("Oumaima", 24, "Female", 24595, Department.NURSE)
    start_date_time = datetime.now()  # Assuming the shift starts now
    end_date_time = datetime.now()  # Assuming the shift ends now
    shift_type = ShiftType.DAY

    monday = Shift(start_date_time, end_date_time, shift_type)
    task = Task("Surgery", inpatient, 2)
    NurseController.perform_task(nurse)


if __name__ == "__main__":
    main()