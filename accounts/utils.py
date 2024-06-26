
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

def detectUser(user):
    if user.roll == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.roll == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.roll == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
    
def send_verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'please active your account'
    message = render_to_string('accounts/emails/account_verification_email.html',{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_mail = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_mail])
    mail.send()
    
    
def send_password_reset_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'reset password'
    message = render_to_string('accounts/emails/reset_pass_email.html',{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    })
    to_mail = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_mail])
    mail.send()
    
    
def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context['user'].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
    
def send_notification_customer(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()