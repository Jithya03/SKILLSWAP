import secrets

def generate_numeric_otp(length=4):
    """Generate a secure numeric OTP with the given length."""
    max_value = 10 ** length
    otp = secrets.randbelow(max_value)
    return str(otp).zfill(length)