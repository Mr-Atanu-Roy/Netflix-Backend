from django.conf import settings
from django.core.mail import send_mail
from threading import Thread

class SendEmail(Thread):
    '''
    Using threads to send mails
    '''
    
    sender = settings.EMAIL_HOST_USER
    
    def __init__(self, subject, message, *receiver):
        self.recipient_list = [emails for emails in receiver]
        self.subject = subject
        self.message = message
        Thread.__init__(self)
        
    def run(self):
        send_mail(self.subject, self.message, self.sender, self.recipient_list)
    
    

