import django.core.validators
from django import forms
from django.core.mail import send_mail
from django.core.validators import EmailValidator

FULL_NAME_FIELD_ATTRIBUTES = {'placeholder': 'Enter your name...', 'class': 'form-control'}
EMAIL_FIELD_ATTRIBUTES = {'placeholder': 'Enter your email...', 'class': 'form-control'}
SUBJECT_FIELD_ATTRIBUTES = {'placeholder': 'Enter subject...', 'class': 'form-control'}
MESSAGE_FIELD_ATTRIBUTES = {'rows': '5', 'placeholder': 'Enter message...', 'class': 'form-control'}

EMAIL_VALIDATOR_MESSAGE = "Please enter a valid email address."

AWS_AUTHENTICATED_EMAIL = "rothweil.miklos@gmail.com"


class ContactForm(forms.Form):
    sender_full_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs=FULL_NAME_FIELD_ATTRIBUTES))
    sender_email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs=EMAIL_FIELD_ATTRIBUTES),
                                    validators=[EmailValidator(message=EMAIL_VALIDATOR_MESSAGE)])
    sender_subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs=SUBJECT_FIELD_ATTRIBUTES))
    sender_message = forms.CharField(max_length=500, widget=forms.Textarea(attrs=MESSAGE_FIELD_ATTRIBUTES))


class ContactEmail:
    def __init__(self, form: ContactForm):
        self.email_address = form.cleaned_data['sender_email']
        self.subject = form.cleaned_data['sender_subject']
        self.message = self.email_address + '\n' \
                       + form.cleaned_data['sender_message'] + '\n' \
                       + form.cleaned_data['sender_full_name']

    def send_message(self):
        send_mail(subject=self.subject, message=self.message, recipient_list=[AWS_AUTHENTICATED_EMAIL],
                  from_email=AWS_AUTHENTICATED_EMAIL)
