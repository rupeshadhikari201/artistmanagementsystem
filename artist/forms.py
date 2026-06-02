from django import forms
from core.forms.base import TailwindForm

GENDER_CHOICES = [
    ('',  'Select'),
    ('m', 'Male'),
    ('f', 'Female'),
    ('o', 'Other'),
]
ALLOWED_EXTENSIONS = ['.csv']
MAX_FILE_SIZE      = 5 * 1024 * 1024  

current_year = __import__('datetime').date.today().year

YEAR_CHOICES = [('', 'Select Year')] + [
    (y, y) for y in range(current_year, 1899, -1)
]


class ArtistCreateForm(TailwindForm):

    name = forms.CharField(
        max_length=255, 
        required=True, 
        label='Full Name'
    )
    
    dob = forms.DateField(
        required=False, 
        label='Date of Birth',
        widget=forms.DateInput(attrs={
            'placeholder': 'YYYY-MM-DD',
            'id': 'flatpickr-default'
        })
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        required=False, 
        label='Gender'
    )
    
    address = forms.CharField(
        max_length=255, 
        required=False, 
        label='Address'
    )
    
    first_release_year = forms.ChoiceField(
        choices=YEAR_CHOICES, 
        required=False, 
        label='First Release Year'
    )
    
    no_of_albums_released = forms.IntegerField(
        required=False, 
        label='Albums Released',
        min_value=0, 
        initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'})
    )

    def clean_first_release_year(self):
        year = self.cleaned_data.get('first_release_year')
        if not year:
            return None
        return int(year)


class ArtistEditForm(ArtistCreateForm):
    
    name = forms.CharField(
    max_length=255, 
    required=True, 
    label='Full Name'
)
    
    dob = forms.DateField(
        required=False, 
        label='Date of Birth',
        widget=forms.DateInput(attrs={
            'placeholder': 'YYYY-MM-DD',
            'id': 'flatpickr-default'
        })
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, 
        required=False, 
        label='Gender'
    )
    
    address = forms.CharField(
        max_length=255, 
        required=False, 
        label='Address'
    )
    
    first_release_year = forms.ChoiceField(
        choices=YEAR_CHOICES, 
        required=False, 
        label='First Release Year'
    )
    
    no_of_albums_released = forms.IntegerField(
        required=False, 
        label='Albums Released',
        min_value=0, 
        initial=0,
        widget=forms.NumberInput(attrs={'placeholder': '0'})
    )

    def clean_first_release_year(self):
        year = self.cleaned_data.get('first_release_year')
        if not year:
            return None
        return int(year)
    

class ArtistImportForm(TailwindForm):
    
    file = forms.FileField(
        label = 'CSV File',
        help_text = 'Max 5mb file in .csv format'
    )
    
    def clean_file(self):
        
        file = self.cleaned_data['file']
        
        # file validations
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Invalid file type. Please upload .csv file')
        
        if file.size > MAX_FILE_SIZE:
            raise forms.ValidationError('Fill to large. Should be less than 5mb.')
        
        if file.size == 0:
            raise forms.ValidationError('The uploaded file is Empty')
        
        return file