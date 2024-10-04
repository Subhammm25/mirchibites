# from django.core.mail import send_mail
# from .models import OTP
# import random

# class OTP:
#     @staticmethod
#     def generate_otp():
#         return str(random.randint(100000, 999999))  # Generates a 6-digit OTP

# def send_otp_email(user):
#     otp_value = OTP.generate_otp()
    
#     # Update or create OTP in the database
#     OTP.objects.update_or_create(user=user, defaults={'otp': otp_value})

#     # Send email to the user with OTP
#     send_mail(
#         'Your OTP for Account Verification',
#         f'Your OTP is {otp_value}. It is valid for 5 minutes.',
#         'your_email@example.com',  # Replace with your actual email
#         [user.email],
#         fail_silently=False,
#     )
