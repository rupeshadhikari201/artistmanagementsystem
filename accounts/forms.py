from django import forms 

from core.forms.base import TailwindForm
from core.utils.turnstile import verify_turnstile

ROLE_CHOICES = [
    ('artist', 'Artist'),
    ('artist_manager', 'Artist Manager'),
    ('super_admin', 'Super Admin')
]

class UserRegisterForm(TailwindForm):
    
    first_name = forms.CharField(
        max_length=255,
        required=True,
        label="First Name"
    )
    
    last_name = forms.CharField(
        max_length=255,
        required=True,
        label="Last Name"
    )
    
    email = forms.EmailField(
        max_length=255,
        required=True,
        label="Email address"
    )
    
    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Phone Number"
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        label="Role"
    )
    
    password = forms.CharField(
        min_length=8,
        required=True,
        label="Password",
        widget=forms.PasswordInput()
    )
    
    confirm_password = forms.CharField(
        required=True,
        label="Confirm Password",
        widget=forms.PasswordInput()
    )

    def clean_email(self):
        from core.db import execute
        email = self.cleaned_data['email'].strip().lower()
        if execute('SELECT id FROM users WHERE email=%s', (email,), fetch='one'):
            raise forms.ValidationError('Email already in use.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not phone:
            raise forms.ValidationError('Phone is required.')

        cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
        if len(cleaned) < 10:
            raise forms.ValidationError('Enter a valid phone number (min 10 digits).')
        return cleaned

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
            
        token = self.data.get("cf-turnstile-response")
        
        if not verify_turnstile(token):
            raise forms.ValidationError("Security check failed. Please try again.")
        
        return cleaned
    

class UserLoginForm(TailwindForm):

    email            = forms.EmailField(max_length=255)
    password         = forms.CharField(min_length=8)
    
    def clean_email(self):
        from core.db import execute
        email = self.cleaned_data['email'].strip().lower()

        user = execute(
            'SELECT id FROM users WHERE email=%s',
            (email,),
            fetch='one'
        )

        if not user:
            raise forms.ValidationError("Email or Password does match.")

        return email

    def clean(self):
        cleaned = super().clean()
        
        token = self.data.get("cf-turnstile-response")
        
        if not verify_turnstile(token):
            raise forms.ValidationError("Security check failed. Please try again.")
        
        return cleaned
