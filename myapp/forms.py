# ...existing code...
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Participant, CleanupEvent, CleanupRegistration

class CleanupEventForm(forms.ModelForm):
    class Meta:
        model = CleanupEvent
        fields = ['name', 'place', 'specific_location', 'date', 'start_time', 
                  'duration', 'points', 'max_participants', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'

class ParticipantRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
        min_length=6,
        label='Password',
        help_text='Password must be at least 6 characters long'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        label='Confirm Password'
    )

    class Meta:
        model = Participant
        fields = ['fullname', 'username', 'email', 'address', 'birthdate', 'contact_number']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'birthdate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number', '')
        if contact_number and not contact_number.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise forms.ValidationError("Contact number must contain only digits, spaces, hyphens, or plus sign.")
        return contact_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Participant.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        participant = super().save(commit=False)
        pw = self.cleaned_data.get('password')
        if pw:
            # if model provides set_password (e.g., extends AbstractBaseUser)
            if hasattr(participant, 'set_password'):
                participant.set_password(pw)
            else:
                participant.password = make_password(pw)
        if commit:
            participant.save()
        return participant
# ...existing code...
class VolunteerLoginForm(forms.Form):
    identifier = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Volunteer email or admin username'
        }),
        label='Email / Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label='Password'
    )
