from django import forms

from .models import *


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        print('send_email')


class FF(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('salutation', 'name', 'email', 'd')

        widgets = {
            'salutation': forms.TextInput(),
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'd': forms.NumberInput()}

class FF2(forms.Form):
    name = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())
    message = forms.CharField(widget=forms.Textarea())


    def send_email(self):
        print(f'sent a massage')
