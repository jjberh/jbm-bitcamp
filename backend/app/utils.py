import re

def is_umd_email(email):

    return re.match(r"^[a-zA-Z0-9]+@(terpmail\.)*umd\.edu$", email)
