from celery import shared_task
from django.core.mail import EmailMessage

from tastybook import settings


@shared_task
def send_email_task(user, email_body):
    from_email = settings.EMAIL_HOST_USER
    data = {'to_email': user.email,
            'from_email': from_email,
            'email_body': email_body,
            'email_subject': "Recipe update"}
    email = EmailMessage(subject=data['email_subject'], body=data['email_body'], from_email=data['from_email'],
                         to=(data['to_email'],))
    email.send()
