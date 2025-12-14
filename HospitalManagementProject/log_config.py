# log_config.py
import logging


def setup_logging():
    # Create a custom logger
    logger = logging.getLogger('HospitalManagement')
    logger.setLevel(logging.DEBUG)  # Set minimum log level to DEBUG for the logger

    # Create handlers for both console and file
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('hospital_management.log')

    # Set levels for handlers
    c_handler.setLevel(logging.WARNING)  # Console handler for warnings and above
    f_handler.setLevel(logging.DEBUG)  # File handler for debug and above messages

    # Create formatters and add them to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

