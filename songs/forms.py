from django import forms
from core.forms.base import TailwindForm

GENRE_CHOICES = [
    ('',  'Select'),
    ('rnb', 'RNB'),
    ('country', 'Country'),
    ('classic', 'Classic'),
    ('rock', 'Rock'),
    ('jazz', 'Jazz'),
]

class MusicCreateForm(TailwindForm):

    title = forms.CharField(
        max_length=255, 
        required=True, 
        label='Title Name'
    )

    album_name = forms.CharField(
        max_length=255, 
        required=True, 
        label='Album Name'
    )
    
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES, 
        required=False, 
        label='Genre'
    )
    

class MusicEditForm(MusicCreateForm):

    title = forms.CharField(
        max_length=255, 
        required=True, 
        label='Title'
    )

    album_name = forms.CharField(
        max_length=255, 
        required=True, 
        label='Album Name'
    )
    
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES, 
        required=False, 
        label='Genre'
    )