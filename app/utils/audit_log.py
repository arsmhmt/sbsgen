import logging
from datetime import datetime

logging.basicConfig(filename='audit.log', level=logging.INFO, format='%(asctime)s %(message)s')

def log_email_send(email, success, reason=None):
    msg = f"EMAIL_SEND | email={email} | success={success}"
    if reason:
        msg += f" | reason={reason}"
    logging.info(msg)

def log_verification_attempt(email, success, reason=None):
    msg = f"VERIFY_ATTEMPT | email={email} | success={success}"
    if reason:
        msg += f" | reason={reason}"
    logging.info(msg)
