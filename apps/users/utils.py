import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings



def generateOtp():

    otp = ''
    for i in range(6):
        otp += str(random.randint(1, 9))
    return otp

def send_code_to_user(email):

    Subject = 'One time passcode for email verification'
    otp_code = generateOtp()
    print(otp_code)
    user = User.objects.get(email=email)
    current_site = 'myauth.com'
    email_body = f'''
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 30px;">
        <div style="max-width: 500px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #eee; padding: 30px;">
            <h2 style="color: #2d7efb;">Welcome to {current_site}!</h2>
            <p style="font-size: 16px; color: #333;">Hi <strong>{user.first_name}</strong>,</p>
            <p style="font-size: 16px; color: #333;">Thanks for signing up. Please verify your email address using the one-time passcode below:</p>
            <div style="text-align: center; margin: 30px 0;">
                <span style="font-size: 32px; letter-spacing: 8px; color: #2d7efb; font-weight: bold;">{otp_code}</span>
            </div>
            <p style="font-size: 16px; color: #333;">Or click the link below to verify:</p>
            <p><a href="http://localhost:8000/api/users/verify-email/" style="color: #2d7efb; text-decoration: underline;">Verify Email</a></p>
            <p style="font-size: 14px; color: #888; margin-top: 40px;">If you did not request this, please ignore this email.</p>
        </div>
    </body>
    </html>
    '''
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)

    d_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    d_email.content_subtype = "html"  # Send as HTML
    d_email.send(fail_silently=False)

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

