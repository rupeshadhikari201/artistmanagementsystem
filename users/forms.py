from django import forms 
from core.forms.base import TailwindForm

ROLE_CHOICES = [
    ('artist', 'Artist'),
    ('artist_manager', 'Artist Manager'),
    ('super_admin', 'Super Admin')
]

GENDER_CHOICES = [
    ('', 'Select'),
    ('f', 'Female'),
    ('m', 'Male'),
    ('o', 'Other')
]

class UserCreateForm(TailwindForm):
    
    first_name       = forms.CharField(max_length=255)
    last_name        = forms.CharField(max_length=255)
    email            = forms.EmailField(max_length=255)
    phone            = forms.CharField(max_length=20, required=False)
    dob              = forms.DateField(required=False)
    gender           = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    address          = forms.CharField(max_length=255, required=False)
    role             = forms.ChoiceField(choices=ROLE_CHOICES)
    password         = forms.CharField(min_length=8)
    confirm_password = forms.CharField()

    def clean_email(self):
        from core.db import execute
        email = self.cleaned_data['email'].strip().lower()
        if execute('SELECT id FROM users WHERE email=%s', (email,), fetch='one'):
            raise forms.ValidationError('Email already in use.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned