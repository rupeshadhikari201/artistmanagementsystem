import bcrypt
from django.shortcuts import render

from .forms import UserCreateForm
from .queries import create_user

def user_create(request):
    
    form = UserCreateForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        data  = form.cleaned_data
        hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = create_user(data, hashed)
        
        return True
        
        
    return render(
        request, 
        'users/create_user.html',
        {
            'form' : form,
            'user' : request.session['user'],
            'action' : 'Create'
        }
    )
