import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def log_attack(attempt_type, input_data):
    """
    Log potential attack attempts.
    """
    logging.warning(f"Possible {attempt_type} attack detected with input: {input_data}")



