from log_config import setup_logging
from controllers.database_controller import DatabaseController
from controllers.patient_controller import PatientController

logger = setup_logging()


class DoctorController:

        @staticmethod
        def add_doctor(db_controller, doctor):
            db_controller.initialize_database()
            try:
                # Check if the doctor already exists in the database
                sql_query = "SELECT id FROM doctors WHERE full_name = ?"
                existing_doctor = db_controller.query(sql_query, (doctor.full_name,))
                if existing_doctor:
                    logger.warning(f"Doctor already exists in the database: {doctor.full_name}")
                    return False

                # Prepare the values for insertion
                department = doctor.display_department()
                values = (
                    doctor.work_id,  # Assuming work_id is provided when creating the Doctor object
                    doctor.full_name, doctor.age, doctor.gender, department,
                    doctor.specialization
                )

                # Insert the doctor into the database
                sql_insert = """
                           INSERT INTO doctors (work_id, full_name, age, gender, department, specialization)
                           VALUES (?, ?, ?, ?, ?, ?)
                           """
                db_controller.insert_record(sql_insert, values)

                logger.info(f"Doctor added successfully: {doctor.full_name}")
                return True
            except Exception as e:
                logger.error(f"Error adding doctor: {e}")
                return False

        @staticmethod
        def remove_doctor(db_controller, doctor):
            try:
                # Find the doctor ID by name
                doctor_id = DoctorController.find_doctor_id_by_name(db_controller, doctor.full_name)
                if doctor_id is None:
                    logger.warning(f"Doctor {doctor.full_name} not found in the database.")
                    return False

                # Remove the doctor from the database
                sql_delete_doctor = "DELETE FROM doctors WHERE id = ?"
                db_controller.delete_record(sql_delete_doctor, (doctor_id,))
                logger.info(f"Doctor {doctor.full_name} removed successfully.")
                return True
            except Exception as e:
                logger.error(f"Error removing doctor: {e}")
                return False

        @staticmethod
        def find_doctor_id_by_name(db_controller, full_name):
            try:
                # Define the SQL SELECT statement to retrieve the doctor's ID
                sql_select = "SELECT id FROM doctors WHERE full_name = ?"

                # Execute the SQL query
                result = db_controller.query(sql_select, (full_name,))

                if result:
                    # Return the doctor's ID if found
                    return result[0][0]
                else:
                    # Return None if the doctor is not found
                    return None
            except Exception as e:
                logger.error(f"Error finding doctor ID: {e}")
                return None

        @staticmethod
        def create_appointment(db_controller, doctor, appointment):
            try:
                doctor_id = DoctorController.find_doctor_id_by_name(doctor.full_name)
                patient_id = PatientController.find_patient_id_by_name(db_controller, appointment.patient.full_name)
                if doctor_id is None:
                    logger.warning(f"Doctor {doctor.full_name} not found in the database.")
                    return False
                if patient_id is None:
                    logger.warning(f"Patient {appointment.patient.full_name} not found in the database.")
                    return False
                else:
                    description = appointment.description
                    date_time = appointment.date_time
                    appointment_type = appointment.appointment_type.value

                    sql_insert = """
                                    INSERT INTO appointments (description, date_time, appointment_type, patient_id, doctor_id)
                                    VALUES (?, ?, ?, ?, ?)
                                """
                    values = (description, date_time, appointment_type, patient_id, doctor_id)
                    db_controller.insert_record(sql_insert, values)
                    doctor.assign_task(appointment)
                    logger.info("Appointment created successfully.")
                    return True

            except Exception as e:
                logger.error(f"Error creating appointment: {e}")
                return False

        @staticmethod
        def perform_duty(db_controller, doctor):
            try:
                if doctor.appointments:
                    # Pop the last appointment
                    appointment = doctor.perform_duty()
                    # Mark the appointment as completed
                    appointment.mark_completed()

                    # Update the is_completed status in the database
                    sql_update = "UPDATE appointments SET is_completed = ? WHERE appointment_id = ?"
                    values = (1, appointment.appointment_id)  # Marking as completed (1)
                    db_controller.update_record(sql_update, values)

                    logger.info(f"Appointment completed and removed: {appointment.description}")
                    return True
                else:
                    logger.info("No upcoming appointments for the doctor.")
                    return False
            except Exception as e:
                logger.error(f"Error performing duty: {e}")
                return False

        @staticmethod
        def prescribe(db_controller, patient, entry):
            try:
                # Check if the patient exists
                patient_id = PatientController.find_patient_id_by_name(db_controller, patient.full_name)
                if patient_id is None:
                    logger.warning(f"Patient {patient.full_name} not found in the database.")
                    return False

                # Provide treatment to the patient
                treatment_successful = PatientController.provide_treatment(patient, entry)
                if treatment_successful:
                    logger.info(f"Prescription provided to patient: {patient.full_name}")
                    return True
                else:
                    logger.error("Failed to provide prescription.")
                    return False
            except Exception as e:
                logger.error(f"Error prescribing medication: {e}")
                return False


