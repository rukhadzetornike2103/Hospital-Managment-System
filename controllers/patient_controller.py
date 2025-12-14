# patient_controller.py
from models.inpatient_model import InPatient
from models.outpatient_model import OutPatient
from models.payment_method import Card
from log_config import setup_logging
from datetime import datetime

from controllers.database_controller import DatabaseController

logger = setup_logging()


class PatientController:
    @staticmethod
    def add_patient(db_controller, patient):
        db_controller.initialize_database()
        try:
            # Check if the patient already exists in the database
            sql_query = "SELECT id FROM patients WHERE full_name = ?"
            existing_patient = db_controller.query(sql_query, (patient.full_name,))
            if existing_patient:
                logger.warning(f"Patient already exists in the database: {patient.full_name}")
                return False

            # Prepare the values, ensuring all are in a compatible format
            condition_value = patient.display_condition()
            admission_value = patient.display_admission_status()
            unique_identifier = patient.generate_unique_identifier()
            if isinstance(patient, InPatient):
                if not PatientController.add_room(db_controller, patient.room):
                    logger.error("Failed to add or update room for the patient.")
                    return False

                sql_insert = """
                        INSERT INTO inpatients (
                            unique_identifier, full_name, age, gender, contact_info, personal_number,
                            insurance, condition, room_number, admission_status
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                values = (
                    unique_identifier, patient.full_name, patient.age, patient.gender, patient.contact_info,
                    patient.personal_number, patient.insurance, condition_value,
                    patient.room.room_number, admission_value
                )
            elif isinstance(patient, OutPatient):
                sql_insert = """
                        INSERT INTO outpatients (
                            unique_identifier, full_name, age, gender, contact_info, personal_number,
                            insurance, condition, admission_status
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                values = (
                    unique_identifier, patient.full_name, patient.age, patient.gender, patient.contact_info,
                    patient.personal_number, patient.insurance, condition_value,
                    admission_value
                )
            else:
                logger.error("Invalid patient type provided.")
                return False

            # Execute the insertion
            if db_controller.insert_record(sql_insert, values):
                logger.info(f"New patient added successfully: {patient.full_name}")
                return True
            else:
                logger.error("Failed to add the patient to the database.")
                return False

        except Exception as e:
            logger.error(f"Error adding patient: {e}")
            return False

    @staticmethod
    def find_patient_id_by_name(db_controller, full_name):
        """
            Search for a patient's ID based on their full name in both inpatients and outpatients tables.

            Args:
                db_controller (DatabaseController): The controller managing database operations.
                full_name (str): The full name of the patient.

            Returns:
                int or None: The patient's ID if found, otherwise None.
            """
        try:
            # First, try to find the patient in the inpatients table
            inpatient_sql = "SELECT id FROM inpatients WHERE full_name = ?"
            with db_controller.connect() as cursor:
                cursor.execute(inpatient_sql, (full_name,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # Return the ID

            # If not found, try the outpatients table
            outpatient_sql = "SELECT id FROM outpatients WHERE full_name = ?"
            with db_controller.connect() as cursor:
                cursor.execute(outpatient_sql, (full_name,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # Return the ID

        except Exception as e:
            logger.error(f"Failed to find patient ID for {full_name}: {e}")

        return None  # Return None if no patient is found

    @staticmethod
    def remove_patient(db_controller, patient):
        """
            Remove a patient from the database after ensuring they are discharged.
            Additionally, update room occupancy for inpatients.

            Args:
                db_controller (DatabaseController): Controller handling database operations.
                patient (InPatient or OutPatient): The patient object to remove.

            Returns:
                bool: True if the patient was successfully removed, False otherwise.
            """
        try:
            # Begin transaction
            with db_controller.connect(True) as cursor:
                # Discharge the patient if not already discharged
                if patient.admission_status != 'Discharged':
                    patient.discharge()  # This method should update the object's admission_status to 'Discharged'
                    update_status_sql = f"UPDATE {type(patient).__name__.lower()}s SET admission_status = 'Discharged' WHERE id = ?"
                    cursor.execute(update_status_sql, (PatientController.find_patient_id_by_name(db_controller, patient.full_name),))

                # If the patient is an inpatient, update room occupancy
                if isinstance(patient, InPatient):
                    update_room_sql = "UPDATE rooms SET is_occupied = 0 WHERE room_number = ?"
                    cursor.execute(update_room_sql, (patient.room.room_number,))

                # Delete the patient record
                delete_sql = f"DELETE FROM {type(patient).__name__.lower()}s WHERE id = ?"
                cursor.execute(delete_sql, (PatientController.find_patient_id_by_name(db_controller, patient.full_name),))

            logger.info(f"Patient removed successfully: {patient.full_name} (ID: {PatientController.find_patient_id_by_name(db_controller, patient.full_name)})")
            return True

        except Exception as e:
            logger.error(f"Error removing patient: {e}")
            return False

    @staticmethod
    def add_room(db_controller, room):
        try:
            # Check if the room already exists
            sql_check_room = "SELECT COUNT(*) FROM rooms WHERE room_number = ?"
            result = db_controller.query(sql_check_room, (room.room_number,))
            room_exists = result[0][0] > 0

            if room_exists:
                # Room already exists, update it
                sql_update_room = """
                        UPDATE rooms 
                        SET room_type = ?, daily_rate = ?, capacity = ?, is_occupied = ? 
                        WHERE room_number = ?
                    """
                values = (
                    room.room_type, room.daily_rate, room.capacity, 1 if room.is_occupied else 0, room.room_number)
                db_controller.update_record(sql_update_room, values)
            else:
                # Room doesn't exist, insert it
                sql_insert_room = """
                        INSERT INTO rooms (room_number, room_type, daily_rate, capacity, is_occupied)
                        VALUES (?, ?, ?, ?, ?)
                    """
                values = (
                    room.room_number, room.room_type, room.daily_rate, room.capacity, 1 if room.is_occupied else 0)
                db_controller.insert_record(sql_insert_room, values)

            logger.debug("Room added or updated successfully.")
            return True
        except Exception as e:
            logger.error(f"Error adding or updating room: {e}")
            return False

    @staticmethod
    def update_room_occupancy(db_controller, room_number, is_occupied):
        try:
            # Define the SQL UPDATE statement for rooms
            sql_update = """
                    UPDATE rooms
                    SET is_occupied = ?
                    WHERE room_number = ?
                """

            # Execute the SQL UPDATE statement using db_controller
            db_controller.update_record(sql_update, (is_occupied, room_number))

            logger.debug("Room occupancy updated successfully.")
            return True
        except Exception as e:
            # Handle any exceptions that may occur
            logger.error(f"Error updating room occupancy: {e}")
            return False

    @staticmethod
    def admit_patient(db_controller, patient):
        try:
            table = 'inpatients' if isinstance(patient, InPatient) else 'outpatients'
            # Check if the patient exists in the database
            sql_check_patient = f"SELECT id FROM {table} WHERE full_name = ?"
            result = db_controller.query(sql_check_patient, (patient.full_name,))
            if result:
                patient_id = result[0][0]
                patient.admit()  # Assumes that the admit method updates the patient object state

                # Update admission status in the database
                sql_update = f"UPDATE {table} SET admission_status = 'Admitted' WHERE id = ?"
                db_controller.update_record(sql_update, (patient_id,))
                logger.info(f"{type(patient).__name__} {patient.full_name} has been admitted.")
            else:
                logger.error(f"{type(patient).__name__} does not exist in the database.")
                return False
            return True
        except Exception as e:
            logger.error(f"Error updating admission status: {e}")
            return False

    @staticmethod
    def remove_room(db_controller, room_number):
        """
            Remove a room from the database by its room number.

            Args:
                db_controller (DatabaseController): The controller handling database operations.
                room_number (int): The room number to remove from the database.

            Returns:
                bool: True if the room was successfully removed, False otherwise.
            """
        try:
            # Define the SQL DELETE statement
            sql_delete = "DELETE FROM rooms WHERE room_number = ?"

            # Execute the SQL DELETE statement using the db_controller
            db_controller.delete_record(sql_delete, (room_number,))
            logger.info("Room removed successfully.")
            return True
        except Exception as e:
            # Handle any exceptions that may occur
            logger.error(f"Error removing room: {e}")
            return False

    @staticmethod
    def discharge_patient(db_controller, patient):
        """
            Discharge a patient and update their admission status and room occupancy in the database.

            Args:
                db_controller (DatabaseController): The controller handling database operations.
                patient (Patient): The patient object to be discharged.

            Returns:
                bool: True if the discharge and database update were successful, False otherwise.
            """
        patient.discharge()  # This method should update the object's admission_status to 'Discharged'

        # Define the basic SQL commands based on the patient type
        if isinstance(patient, InPatient):
            table_name = "inpatients"
            additional_update = "UPDATE rooms SET is_occupied = 0 WHERE room_number = ?"
            additional_params = (patient.room.room_number,)
        elif isinstance(patient, OutPatient):
            table_name = "outpatients"
            additional_update = None
            additional_params = None
        else:
            logger.error("Invalid patient type provided.")
            return False

        try:
            # Check if the patient exists in the database
            sql_check_patient = f"SELECT id FROM {table_name} WHERE full_name = ?"
            result = db_controller.query(sql_check_patient, (patient.full_name,))
            if result:
                # Patient exists, update admission status in the database
                patient_id = result[0][0]
                sql_update = f"UPDATE {table_name} SET admission_status = 'Discharged' WHERE id = ?"
                db_controller.update_record(sql_update, (patient_id,))

                # If there's an additional action required (e.g., updating room status for inpatients)
                if additional_update:
                    db_controller.update_record(additional_update, additional_params)

                logger.info(f"Patient {patient.full_name} successfully discharged.")
                return True
            else:
                logger.error(f"No existing record for patient {patient.full_name} in the database.")
                return False

        except Exception as e:
            logger.error(f"Error during the discharge process: {e}")
            return False

    @staticmethod
    def provide_treatment(patient, entry):
        if not isinstance(entry, str):
            logger.warning("Invalid entry type provided for treatment details.")
            return False

        try:
            patient.provide_treatment_details(entry)
            logger.debug(f"Treatment details added to patient record: {entry}")
            return True
        except AttributeError:
            # This error might occur if the patient object doesn't have the 'provide_treatment_details' method
            logger.error("Patient object does not support the addition of treatment details.")
            return False
        except Exception as e:
            # Handle any other exceptions that could occur
            logger.error(f"An error occurred while adding treatment details: {e}")
            return False

    @staticmethod
    def add_card(patient, card):
        # Check if the 'card' object is an instance of the Card class
        if not isinstance(card, Card):
            logger.warning("Attempt to add a non-card object as a payment method.")
            return False

        try:
            patient.add_payment_method(card)
            logger.debug("Card added successfully to patient's profile.")
            return True
        except Exception as e:
            logger.error(f"Failed to add card due to an error: {e}")
            return False

    @staticmethod
    def deposit(patient, amount):
        if len(patient.cards) == 0:
            logger.error("You must add a card first.")
            return False  # Explicit return to indicate the operation was unsuccessful

        if amount <= 1:
            logger.error("You cannot deposit less than $1.")
            return False  # Explicit return to indicate the operation was unsuccessful

        try:
            patient.balance += amount
            logger.info(f"Deposited ${amount} | Current balance: ${patient.balance}")
            return True  # Indicate successful deposit
        except Exception as e:
            logger.error(f"An error occurred while updating the balance: {e}")
            return False  # Return False in case of an exception to indicate failure

    @staticmethod
    def charge(patient, amount):
        if amount < 1:
            logger.error("Amount cannot be less than $1.")
            return False
        try:
            # Assume patient.charge(amount) method exists and performs the charging operation
            patient.charge(amount)
            logger.info(f"Patient {patient.full_name} charged successfully: ${amount}.")
            return True
        except AttributeError:
            # If the patient object does not have a charge method
            logger.error(f"Patient object does not support charging. Attempted to charge ${amount}.")
            return False
        except Exception as e:
            # General error handling for any other unexpected issues during the charge operation
            logger.error(f"An error occurred while attempting to charge patient {patient.full_name}: {e}")
            return False

    @staticmethod
    def add_medical_history(db_controller, patient, entry):
        try:
            # Check if the patient exists in the database
            patient_id = PatientController.find_patient_id_by_name(db_controller, patient.full_name)
            if not patient_id:
                logger.error("Patient not found in the database.")
                return False

            # Add the medical history entry to the patient's local medical history
            patient.add_medical_history(entry)

            # Insert the medical history entry into the database
            sql_insert = """
                    INSERT INTO medical_history (patient_id, entry, date_added)
                    VALUES (?, ?, ?)
                    """
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_controller.insert_record(sql_insert, (patient_id, entry, current_datetime))

            logger.info("Medical history entry added successfully.")
            return True
        except Exception as e:
            logger.error(f"Error adding medical history entry: {e}")
            return False

