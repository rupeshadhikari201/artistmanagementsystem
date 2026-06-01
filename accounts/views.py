import bcrypt
import logging
from django.shortcuts import render, redirect

from  core.db import execute
from .forms import UserRegisterForm, UserLoginForm
from .queries import user_register

logger = logging.getLogger(__name__)

def register_view(request):
    
    if request.session.get('user'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data

            try:
                hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
                user = user_register(data, hashed)
                
                if user:
                    logger.info('User registered successfully. id=%s', user['id'])
                    return redirect('login')
                else:
                    logger.error('user_register returned None for email: %s', data['email'])
                    form.add_error(None, 'Registration failed. Please try again')
            
            except Exception as e:
                logger.exception('Unexpected error during registration: %s', str(e))
                form.add_error(None, 'Something went wrong. Please try again later.')
    
    else:
        form = UserRegisterForm()
        
    return render(
        request, 
        'register.html',
        {
            'form' : form
        }
    )

    
def login_view(request):
    
    if request.session.get('user'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            email    = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']
            
            try:
                
                user = execute(
                    'select * from users where email = %s',
                    (email,),
                    fetch='one'
                )
                
                if not  user or not bcrypt.checkpw(password.encode(),user['password'].encode()):
                    logger.warning('Failed login attempt for email: %s', email)
                    form.add_error(None, 'Invalid email or password.')
                    return render(request, 'login.html', {'form': form})
                
                request.session['user'] = {
                    'id':         user['id'],
                    'first_name': user['first_name'],
                    'last_name':  user['last_name'],
                    'email':      user['email'],
                    'role':       user['role'],
                }
                
                logger.info('User logged in. id=%s role=%s', user['id'], user['role'])
                return redirect('dashboard')
            
            except Exception as e:
                logger.exception('Unexpected error during login: %s', str(e))
                form.add_error(None, 'Something went wrong. Please try again later.')
        
    else:
        form = UserLoginForm()   

    return render(
        request,
        'login.html',
        {
            'form' : form
        }
    )

    
def logout_view(request):
    user = request.session.get('user',{})
    logger.info('User logged out. id=%s', user.get('id'))
    request.session.flush()
    return redirect('login')