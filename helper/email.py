import datetime
from django.core.mail import send_mail,BadHeaderError,EmailMessage
from django.template.loader import render_to_string
from helper.Constants import MAIL_TEMPLATE_PATH

def welcome(name, email):
    context={
        'name':name,
        }
    html_message = render_to_string(MAIL_TEMPLATE_PATH+'welcome.html', context=context)
    send_mail("Welcome",'','travelmates247@gmail.com',[email],html_message=html_message,fail_silently=True)

def welcome_wtih_credentials(name, email, phone, password):
    context={
        'name':name,
        'phone':phone,
        'password':password,
        }
    html_message = render_to_string(MAIL_TEMPLATE_PATH+'welcome_with_c.html', context=context)
    send_mail("Welcome",'','travelmates247@gmail.com',[email],html_message=html_message,fail_silently=True)

def password_change(name, email, phone):
    context={
        'name':name,
        'phone':phone,
        'email':email,
        'date':datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        }
    html_message = render_to_string(MAIL_TEMPLATE_PATH+'password_change.html', context=context)
    send_mail("Password Changed",'','travelmates247@gmail.com',[email],html_message=html_message,fail_silently=True)

def send_otp(name, email, otp):
    context={
        'name':name,
        'otp':otp,
        }
    html_message = render_to_string(MAIL_TEMPLATE_PATH+'otp.html', context=context)
    send_mail("Welcome",'','travelmates247@gmail.com',[email],html_message=html_message,fail_silently=True)
