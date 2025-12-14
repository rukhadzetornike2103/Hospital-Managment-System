from log_config import setup_logging
from controllers.database_controller import DatabaseController
from controllers.patient_controller import PatientController
logger = setup_logging()
db_controller = DatabaseController()


class NurseController:
        @staticmethod
        def add_nurse(nurse):
            try:
                # Check if the nurse already exists in the database
                sql_query = "SELECT work_id FROM nurses WHERE full_name = ?"
                existing_nurse = db_controller.query(sql_query, (nurse.full_name,))
                if existing_nurse:
                    logger.warning(f"Nurse already exists in the database: {nurse.full_name}")
                    return False

                # Prepare the values for insertion
                department = nurse.display_department()
                values = (
                    nurse.work_id, nurse.full_name, nurse.age, nurse.gender, department
                )

                # Insert the nurse into the database
                sql_insert = """
                                INSERT INTO nurses (work_id, full_name, age, gender, department)
                                VALUES (?, ?, ?, ?, ?)
                                """
                db_controller.insert_record(sql_insert, values)

                logger.info(f"Nurse added successfully: {nurse.full_name}")
                return True
            except Exception as e:
                logger.error(f"Error adding nurse: {e}")
                return False

        @staticmethod
        def find_nurse_id_by_name(full_name):
            try:
                # Query the database to find the nurse's ID by full name
                sql_query = "SELECT id FROM nurses WHERE full_name = ?"
                result = db_controller.query(sql_query, (full_name,))

                if result:
                    return result[0][0]  # Return the nurse's ID if found
                else:
                    logger.warning(f"No nurse found with name: {full_name}")
                    return None
            except Exception as e:
                logger.error(f"Error finding nurse by name: {e}")
                return None

        @staticmethod
        def remove_nurse(nurse):
            try:
                # Find the doctor ID by name
                nurse_id = NurseController.find_nurse_id_by_name(nurse.full_name)
                if nurse_id is None:
                    logger.warning(f"Doctor {nurse.full_name} not found in the database.")
                    return False

                # Remove the doctor from the database
                sql_delete_nurse = "DELETE FROM nurses WHERE id = ?"
                db_controller.delete_record(sql_delete_nurse, (nurse_id,))
                logger.info(f"Doctor {nurse.full_name} removed successfully.")
                return True
            except Exception as e:
                logger.error(f"Error removing doctor: {e}")
                return False

        @staticmethod
        def assign_task(nurse, new_task):
            try:
                patient_id = PatientController.find_patient_id_by_name(db_controller, new_task.patient.full_name)
                if patient_id is not None:
                    # Insert the task into the tasks table
                    sql_insert = """
                               INSERT INTO tasks (description, patient_id, priority)
                               VALUES (?, ?, ?)
                           """
                    values = (new_task.description, patient_id, new_task.priority)
                    task_id = db_controller.insert_record(sql_insert, values)

                    if task_id:
                        # Assign the task to the nurse
                        nurse.assign_task(new_task)
                        logger.info(f"Task assigned to Nurse {nurse.full_name}")
                        return True
                    else:
                        logger.error("Failed to assign task.")
                        return False
                else:
                    logger.error("Patient not found.")
                    return False
            except Exception as e:
                logger.error(f"Error assigning task: {e}")
                return False

        @staticmethod
        def perform_task(nurse):
            try:
                if nurse.assigned_tasks:  # Update this line to match the attribute name
                    # Get the highest priority task
                    sorted_tasks = sorted(nurse.assigned_tasks, key=lambda x: x.priority)
                    highest_priority_task = sorted_tasks[0]

                    # Mark the task as completed
                    highest_priority_task.mark_completed()

                    # Update the completion status in the database
                    sql_update = "UPDATE tasks SET is_completed = ? WHERE task_id = ?"
                    values = (1, highest_priority_task.task_id)  # Marking as completed (1)
                    db_controller.update_record(sql_update, values)

                    # Remove the task from the nurse's list of assigned tasks
                    nurse.assigned_tasks.remove(highest_priority_task)  # Update this line

                    logger.info(f"Task performed and marked as completed: {highest_priority_task.description}")
                    return True
                else:
                    logger.info("No tasks assigned to the nurse.")
                    return False
            except Exception as e:
                logger.error(f"Error performing task: {e}")
                return False

        @staticmethod
        def add_shift(nurse, shift):
            try:
                # Insert the shift into the shifts table
                sql_insert = """
                       INSERT INTO shifts (start_date_time, end_date_time, shift_type)
                       VALUES (?, ?, ?)
                   """
                values = (shift.start_date_time.isoformat(), shift.end_date_time.isoformat(), shift.shift_type.value)
                shift_id = db_controller.insert_record(sql_insert, values)

                if shift_id:
                    nurse.add_shift(shift)
                    logger.info(f"Shift added successfully with ID: {shift_id}")
                    return True
                else:
                    logger.error("Failed to add shift to the database.")
                    return False
            except Exception as e:
                logger.error(f"Error adding shift: {e}")
                return False

