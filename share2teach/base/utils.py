# utils.py

import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code(length=6):
    """Generate a random alphanumeric verification code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_verification_code(user):
    # Generate a verification code
    verification_code = generate_verification_code()
    
    # Save the code to the user's profile
    user.verification_code = verification_code
    user.save()

    # Send an email with the verification code
    subject = 'Your Verification Code'
    message = f'Your verification code is: {verification_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
