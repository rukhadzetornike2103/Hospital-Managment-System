import sqlite3
from contextlib import contextmanager
from log_config import setup_logging
from datetime import datetime

logger = setup_logging()


class DatabaseController:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name

    def initialize_database(self):
        self.create_patients_table()
        self.create_inpatients_table()
        self.create_outpatients_table()
        self.create_rooms_table()
        self.create_doctors_table()
        self.create_nurse_table()
        self.create_appointments_table()
        self.create_medical_history_table()
        self.create_tasks_table()
        self.create_shifts_table()

    @contextmanager
    def connect(self, start_transaction = False):
        """Manage database connection, ensuring it is closed after use."""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            if start_transaction:
                cursor.execute('BEGIN;')
            yield cursor
        except Exception as e:
            connection.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        else:
            connection.commit()
        finally:
            connection.close()

    def create_table(self, sql):
        """Creates a table in the database based on the provided SQL statement."""
        try:
            with self.connect() as cursor:
                cursor.execute(sql)
                logger.info("Table created successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to create table: {e}")

    def insert_record(self, sql, params):
        """Inserts a record into the database using the provided SQL statement and parameters."""
        try:
            with self.connect() as cursor:
                cursor.execute(sql, params)
                last_row_id = cursor.lastrowid
                logger.info(f"Record inserted successfully, ID: {last_row_id}")
                return last_row_id
        except sqlite3.Error as e:
            logger.error(f"Failed to insert record: {e}")
            return None

    def query(self, sql, params=None):
        """Executes a SQL query and returns the fetched results."""
        try:
            with self.connect() as cursor:
                cursor.execute(sql, params or ())
                results = cursor.fetchall()
                logger.debug("Query executed successfully.")
                return results
        except sqlite3.Error as e:
            logger.error(f"Failed to execute query: {e}")
            return None

    def update_record(self, sql, params):
        """Updates records in the database."""
        try:
            with self.connect() as cursor:
                cursor.execute(sql, params)
                logger.info("Record updated successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to update record: {e}")

    def delete_record(self, sql, params):
        """Deletes records from the database."""
        try:
            with self.connect() as cursor:
                cursor.execute(sql, params)
                logger.info("Record deleted successfully.")
        except sqlite3.Error as e:
            logger.error(f"Failed to delete record: {e}")

    def run_transaction(self, operations):
        """Runs a set of database operations as a single transaction."""
        try:
            with self.connect() as cursor:
                for sql, params in operations:
                    cursor.execute(sql, params)
                logger.info("Transaction executed successfully.")
                return True
        except sqlite3.Error as e:
            logger.error(f"Transaction failed: {e}")
            return False

    def create_patients_table(self):
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL UNIQUE,
                age INTEGER,
                gender TEXT,
                contact_info TEXT,
                personal_number TEXT,
                insurance TEXT,
                condition TEXT,
                admission_status TEXT
            );
        """
            self.create_table(sql)
        except Exception as e:
            logger.error(f'Error creating table: {e}')

    def create_inpatients_table(self):
        try:
            sql = """
                        CREATE TABLE IF NOT EXISTS inpatients (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            unique_identifier TEXT NOT NULL UNIQUE,
                            full_name TEXT NOT NULL UNIQUE,
                            age INTEGER,
                            gender TEXT,
                            contact_info TEXT,
                            personal_number TEXT,
                            insurance TEXT,
                            condition TEXT,
                            room_number INTEGER,
                            admission_status TEXT,
                            FOREIGN KEY (room_number) REFERENCES rooms(room_number)
                        );
                    """
            self.create_table(sql)

            logger.info("Table 'inpatients' created successfully.")
        except Exception as e:
            # Handle any exceptions that may occur
            logger.error(f"Error creating table: {e}")

    def create_outpatients_table(self):
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS outpatients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_identifier TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL UNIQUE,
                age INTEGER,
                gender TEXT,
                contact_info TEXT,
                personal_number TEXT,
                insurance TEXT,
                condition TEXT,
                admission_status TEXT
            );
        """
            self.create_table(sql)

            logger.info("Table 'outpatients' created successfully.")
        except Exception as e:
            # Handle any exceptions that may occur
            logger.error(f"Error creating table: {e}")

    def create_rooms_table(self):
        try:
            sql = """
    CREATE TABLE IF NOT EXISTS rooms (
        room_number INTEGER PRIMARY KEY,
        room_type TEXT NOT NULL,
        daily_rate REAL NOT NULL,
        capacity INTEGER NOT NULL,
        is_occupied INTEGER NOT NULL DEFAULT 0,
        CHECK (room_type IN ('Single', 'Double', 'ICU')),
        CHECK (daily_rate >= 1),
        CHECK (capacity BETWEEN 1 AND 2),
        CHECK (is_occupied IN (0, 1))
    );
    """
            self.create_table(sql)
        except Exception as e:
            logger.error(f'Error creating table: {e}')

    def create_appointments_table(self):
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    date_time DATETIME NOT NULL,  -- Store as TEXT in ISO8601 format ("YYYY-MM-DD HH:MM:SS")
                    appointment_type TEXT NOT NULL,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    is_completed INTEGER NOT NULL DEFAULT 0,  -- 0 for false, 1 for true
                    FOREIGN KEY (patient_id) REFERENCES patients(id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
                    CHECK (appointment_type IN ('Surgery', 'Consultation', 'Visit', 'Procedure')),
                    CHECK (is_completed IN (0, 1))
                );
                """
            self.create_table(sql)
            logger.info("Appointments table created successfully.")
        except Exception as e:
            logger.error(f'Error creating table: {e}')

    def create_doctors_table(self):
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                department TEXT,
                specialization TEXT NOT NULL
                );
            """
            self.create_table(sql)
            logger.info("Doctors table created successfully.")
        except Exception as e:
            logger.error(f'Error creating table: {e}')

    def create_nurse_table(self):
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS nurses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    work_id INTEGER NOT NULL,
                    full_name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    department TEXT
                );
                """
            self.create_table(sql)
            logger.info("Nurses table created successfully.")
        except Exception as e:
            logger.error(f'Error creating table: {e}')

    def create_medical_history_table(self):
        try:
            sql = """
                    CREATE TABLE IF NOT EXISTS medical_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        entry TEXT NOT NULL,
                        date_added TEXT NOT NULL,
                        FOREIGN KEY (patient_id) REFERENCES patients(id)
                    );
                    """
            self.create_table(sql)
            logger.info("Medical history table created successfully.")
        except Exception as e:
            logger.error(f"Error creating medical history table: {e}")

    def create_tasks_table(self):
        try:
            sql = """
                   CREATE TABLE IF NOT EXISTS tasks (
                       task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       description TEXT NOT NULL,
                       patient_id INTEGER NOT NULL,
                       priority INTEGER NOT NULL,
                       is_completed INTEGER NOT NULL DEFAULT 0,  -- 0 for false, 1 for true
                       FOREIGN KEY (patient_id) REFERENCES patients(id),
                       CHECK (priority >= 0)  -- Ensure priority is non-negative
                   );
               """
            self.create_table(sql)
            logger.info("Tasks table created.")
        except Exception as e:
            logger.error(f'Error creating tasks table: {e}')

    def create_shifts_table(self):
        try:
            sql = """
                    CREATE TABLE IF NOT EXISTS shifts (
                        shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        start_date_time TEXT NOT NULL,
                        end_date_time TEXT NOT NULL,
                        shift_type TEXT NOT NULL
                    );
                """
            self.create_table(sql)
            logger.info("Shifts table created.")
        except Exception as e:
            logger.error(f'Error creating shifts table: {e}')



