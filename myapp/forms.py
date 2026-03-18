from django import forms

from django import forms
from .models import UserProfile

from .models import Career, Category, MenuItem, Review, ContactMessage, NewsletterSubscription, UserProfile

# Form to handle contact messages sent through the contact page
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
    # Validation to prevent temporary email addresses and links in the message
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "tempmail.com" in email:
            raise forms.ValidationError("Please use a permanent email address.")
        return email
    
    # Validation to prevent links and ensure the message is of a reasonable length
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if 'http' in message:
            raise forms.ValidationError("Links are not allowed in the message.")
        if len(message) < 10:
            raise forms.ValidationError("Your message is too short.")
        return message

# Form to handle newsletter subscriptions on the newsletter page
class ReviewForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    rating = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea)

# Form to handle newsletter subscriptions on the newsletter page
class NewsletterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name (Optional)'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))

# Form to handle user profile updates on the profile page
class UserProfileForm(forms.Form):
    address = forms.CharField(max_length=255, required=False)
    telephone_number = forms.CharField(max_length=20, required=False)
    favorite_dessert = forms.CharField(max_length=100, required=False)