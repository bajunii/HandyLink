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
    Subject = 'Verify Your HandyLink Account - Email Verification'
    otp_code = generateOtp()
    print(f"🔑 Generated OTP for {email}: {otp_code}")
    
    try:
        user = User.objects.get(email=email)
        current_site = 'HandyLink'
        
        email_body = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email - HandyLink</title>
        </head>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); overflow: hidden;">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #0a2463 0%, #3e92cc 100%); color: #ffffff; padding: 30px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: bold;">HandyLink</h1>
                    <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9; letter-spacing: 1px;">YOUR TRUSTED SERVICE MARKETPLACE</p>
                </div>
                
                <!-- Body -->
                <div style="padding: 40px 30px;">
                    <h2 style="color: #0a2463; margin-bottom: 20px; font-size: 24px;">🔐 Verify Your Email Address</h2>
                    
                    <p style="font-size: 16px; color: #333; margin-bottom: 20px;">Hi <strong>{user.first_name}</strong>,</p>
                    
                    <p style="font-size: 16px; color: #555; margin-bottom: 30px; line-height: 1.7;">
                        Welcome to HandyLink! To complete your registration and start connecting with trusted service providers, 
                        please verify your email address using the verification code below:
                    </p>
                    
                    <!-- OTP Code -->
                    <div style="background: #f8f9fa; border: 2px dashed #3e92cc; border-radius: 12px; padding: 30px; text-align: center; margin: 30px 0;">
                        <p style="color: #0a2463; font-size: 14px; margin: 0 0 10px 0; font-weight: 600;">YOUR VERIFICATION CODE</p>
                        <div style="font-size: 36px; letter-spacing: 8px; color: #3e92cc; font-weight: bold; font-family: 'Courier New', monospace;">
                            {otp_code}
                        </div>
                        <p style="color: #777; font-size: 12px; margin: 10px 0 0 0;">This code expires in 15 minutes</p>
                    </div>
                    
                    <!-- Instructions -->
                    <div style="background: #e8f4fd; border-left: 4px solid #3e92cc; padding: 20px; margin: 20px 0; border-radius: 0 8px 8px 0;">
                        <p style="color: #0a2463; font-weight: 600; margin: 0 0 10px 0;">📱 How to verify:</p>
                        <ol style="color: #555; margin: 0; padding-left: 20px;">
                            <li>Copy the 6-digit code above</li>
                            <li>Return to the HandyLink app</li>
                            <li>Paste the code in the verification field</li>
                            <li>Click "Verify Email" to activate your account</li>
                        </ol>
                    </div>
                    
                    <!-- Alternative Link -->
                    <div style="text-align: center; margin: 30px 0;">
                        <p style="color: #777; font-size: 14px; margin-bottom: 15px;">Or click the button below to verify:</p>
                        <a href="http://localhost:8000/api/users/verify-email/" 
                           style="background: linear-gradient(135deg, #3e92cc 0%, #2a9d8f 100%); 
                                  color: white; 
                                  padding: 15px 30px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  font-weight: 600; 
                                  display: inline-block;
                                  box-shadow: 0 4px 15px rgba(62, 146, 204, 0.3);">
                            ✅ Verify Email Address
                        </a>
                    </div>
                    
                    <!-- Security Note -->
                    <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 20px 0;">
                        <p style="color: #856404; margin: 0; font-size: 14px;">
                            <strong>🔒 Security Notice:</strong> We sent this code because someone requested to verify this email address for a HandyLink account. 
                            If you didn't make this request, please ignore this email.
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #eee;">
                    <p style="color: #777; margin: 0 0 10px 0; font-size: 14px;">
                        <strong>HandyLink Team</strong><br>
                        Connecting you with trusted service providers
                    </p>
                    <p style="color: #999; font-size: 12px; margin: 0;">
                        You received this email because you signed up for HandyLink.<br>
                        This is an automated message, please do not reply.
                    </p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        from_email = settings.DEFAULT_FROM_EMAIL

        OneTimePassword.objects.create(user=user, code=otp_code)

        d_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
        d_email.content_subtype = "html"  # Send as HTML
        
        # Send the email
        try:
            d_email.send(fail_silently=False)
            print(f"✅ Verification email sent successfully to {email}")
        except Exception as email_error:
            print(f"❌ SMTP Error sending verification email: {email_error}")
            # Still create the OTP even if email fails
            print(f"📱 OTP created for manual verification: {otp_code}")
            raise email_error
        
    except User.DoesNotExist:
        print(f"❌ User with email {email} not found")
        raise
    except Exception as e:
        print(f"❌ Error sending verification email: {e}")
        raise

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

