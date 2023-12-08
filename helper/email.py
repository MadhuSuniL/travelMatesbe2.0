from django.core.mail import send_mail,BadHeaderError,EmailMessage
from django.template.loader import render_to_string
from helper.Constants import MAIL_TEMPLATE_PATH



def welcome(name, email, *args, **kwargs):
    context={
        'name':name,
        }
    html_message = render_to_string(MAIL_TEMPLATE_PATH+'welcome.html', context=context)
    send_mail("Welcome",'','travelmates247@gmail.com',[email],html_message=html_message)
