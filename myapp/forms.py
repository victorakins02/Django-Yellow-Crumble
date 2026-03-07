from django import forms

from .models import Career, Category, MenuItem

class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sarah'}),
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Murphy'}),
        label='Last Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
        label='Email Address'
    )
    subject = forms.ChoiceField(
        choices=[('job', 'Job Application'), ('general', 'General Inquiry')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='What is it about?'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us what is on your mind..'}),
        label='Message'
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "tempmail.com" in email:
            raise forms.ValidationError("Please use a permanent email address.")
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if 'http' in message:
            raise forms.ValidationError("Links are not allowed in the message.")
        if len(message) < 10:
            raise forms.ValidationError("Your message is too short.")
        return message