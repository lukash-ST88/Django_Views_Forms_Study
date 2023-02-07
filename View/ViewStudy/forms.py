from django import forms

from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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
            'salutation': forms.TextInput(attrs={'class': 'form-control', 'id': '{{f.id_for_label}}'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'd': forms.NumberInput(attrs={'class': 'form-control'})}


class FF2(forms.Form):
    name = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())
    message = forms.CharField(widget=forms.Textarea())

    def send_email(self):
        print(f'sent a massage')


"""Forms"""


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()


class MultiEmailField(forms.Field): #создание нового поля
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    recipients = MultiEmailField()
    cc_myself = forms.BooleanField(required=False)

    def clean_recipients(self): # валидация отдельного поля
        data = self.cleaned_data['recipients']
        if "fred@example.com" not in data:
            raise ValidationError("You have forgotten about Fred!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

    def clean(self): # для валидации двух и более зависящих полей
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )