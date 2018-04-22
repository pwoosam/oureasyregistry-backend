from secrets import api_key, customer_id
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits

def send_text(phone_number, message):
    messaging = MessagingClient(customer_id, api_key)
    response = messaging.message(phone_number, message, "ARN")
    return response

def send_two_factor_code(phone_number):  # TODO: Save the phone number and verification code in db
    verify_code = random_with_n_digits(5)

    message = f"Your code is {verify_code}"
    message_type = "OTP"

    messaging = MessagingClient(customer_id, api_key)
    response = messaging.message(phone_number, message, message_type)
    return response

def validate_two_factor_code(phone_number, code_to_test):  # TODO: Get the code for the phone number from the db
    code_from_db = "12345"
    if code_from_db == code_to_test:
        return True
    else:
        return False
