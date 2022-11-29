from django import forms


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget= forms.Textarea)

    def send_email(self):
        print('send_email')

