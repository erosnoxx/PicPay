import secrets


def generate_otp():
    return secrets.randbelow(10**7 - 1) + 10**6
