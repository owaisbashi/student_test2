import time
import random

def generate_student_id():
    # Get the current timestamp
    timestamp = int(time.time())
    # Generate a random number
    rand = random.randint(1, 9)
    # Concatenate the timestamp and the random number
    student_id = f"{timestamp}{rand}"
    return student_id[4:]