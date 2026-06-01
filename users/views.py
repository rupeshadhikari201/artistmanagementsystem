import bcrypt
import logging
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import (
    UserCreateForm,
    UserEditForm,
)
from .queries import (
    create_user, 
    get_users_page,
    get_user_by_id,
    update_user, 
    update_user_password, 
    delete_user,
)

logger = logging.getLogger(__name__)
    

def user_list(request):
    try:
        page = int(request.GET.get('page',1))
        data = get_users_page(page, per_page=5)
        
        return render(
            request,
            'users/list.html',
            {
                **data, 
                'offset' : (data['page'] -1) * data['per_page'],
                'page_range': range(1, data['total_pages'] + 1),
                'user' : request.session.get('user'),
            }
        )
        
    except ValueError as e:
        logger.warning(f"Invalid page value : {e}")
        return render(
            request,
            'users/list.html',
            {
                'rows' : [],
                'error' : 'Invalid page number',
            }
        )
    
    except Exception as e:
        logger.exception("User list failed")
        return render(request, 'users/list.html', {
            'rows': [],
            'error': 'Something went wrong. Please try again later.',
        })
    
        
def user_create(request):
    
    if request.method == 'POST':
        
        form = UserCreateForm(request.POST)
        
        if form.is_valid():
            data  = form.cleaned_data
            
            try:
                hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
                user = create_user(data, hashed)
                
                if user:
                    logger.info('User created successfully.')
                    return redirect('users-list')
                else:                   
                    logger.error('create_user returned None for email: %s', data['email'])
                    form.add_error(None, 'User creation failed. Please try again')
            
            except Exception as e:
                logger.exception("User creation failed")
                form.add_error(None, 'Something went wrong. Please try again later.')
            
    else:
        form = UserCreateForm()
        
        
    return render(
        request, 
        'users/create.html',
        {
            'form' : form,
        }
    )
    
    
def user_edit(request, user_id):
    target = get_user_by_id(user_id)
    
    if not target:
        logger.warning(request, 'User not found.')
        return redirect('users-list')
    
    if request.method == 'POST':
        
        form = UserEditForm(request.POST, current_user_id=user_id)
        
        if form.is_valid():
            data = form.cleaned_data
            
            try:
                update_user(user_id, data)
                
                if data.get('password'):
                    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
                    update_user_password(user_id, hashed)
                       
                logger.info("User updated successfully. id=%s", user_id)
                messages.success(request, 'User updated successfully.')
                return redirect('users-list')
            
            except Exception as e:
                logger.exception("User update failed for id: %s", user_id)
                form.add_error(None, 'Something went wrong. Please try again later.')
                
    else:
        form = UserEditForm(
            initial = {
                k : target.get(k, '') for k in ['first_name', 'last_name', 'email', 'phone', 'dob', 'gender', 'address', 'role']
            },
            current_user_id=user_id
        )
        
    return render(
        request, 
        'users/edit.html',
        {
            'form' : form,
            'target' : target,
            'user_id' : user_id,
        }   
    )
   
    
def user_delete(request, user_id):
    
    if request.method == 'POST':
        
        try:
            target  = get_user_by_id(user_id)
            
            if target:
                delete_user(user_id)
                logger.info("User deleted successfully. id=%s", user_id)
                messages.success(request, 'User deleted successfully.')
            else:
                logger.warning("User not found for deletion. id=%s", user_id)
                messages.error(request, 'User not found.')  
        except Exception as e:
            logger.exception('user_delete failed: %s', str(e))
            messages.error(request, 'Something went wrong.')

    return redirect('users-list')
    