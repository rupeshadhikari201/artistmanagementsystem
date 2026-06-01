import logging

from core.db import execute
from core.pagination import paginate

logger = logging.getLogger(__name__)


def create_user(data, hashed_password):
    
    user = execute(
        """
            insert into users 
            (first_name, last_name, email, password, phone, dob, gender, address,role )
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            returning id
        """,
        (
            data['first_name'],
            data['last_name'],
            data['email'],
            hashed_password,
            data.get('phone') or None, 
            data.get('dob') or None,
            data.get('gender') or None,
            data.get('address') or None,
            data['role'],
        ),
        fetch='one'
        
    )
    
    return user   


def get_users_page(page, per_page=10):
    """
    Fetch users data paginated. 
    
    Params: 
        page(int) : current page no requested. 
        
        per_page(int) : no of record per page
        
    Returns:
        Return a dict of pagination metadata
    
    """
    
    try:
        pagination = paginate(
            sql_count = 'select count(*) as count from users',
            sql_data = '''
                select id, first_name, last_name, email, role, phone, gender, created_at
                from users
                order by created_at desc
                limit %s offset %s
            ''',
            params=(),
            page=page,
            per_page=per_page
            
        )
        return pagination
    
    except Exception as e:
        logger.exception("Pagination failed for get_users_page.")
        return {
            'rows': [],
            'page': 1,
            'per_page': per_page,
            'total': 0,
            'total_pages': 1,
            'has_prev': False,
            'has_next': False,
        }
        

def get_user_by_id(user_id):
    """
    Fetch user by id. Return None if not found.
    """
    
    user = execute(
        'select * from users where id = %s', 
        (user_id,),
        fetch='one'
    )
    
    return user
    

def update_user(user_id, data):
    """
    Update user by id. 
    Return True if update is successful, False otherwise.
    """
    
    execute(
        """
        update users  
        set first_name = %s, last_name = %s, email = %s, 
            phone = %s, dob = %s, gender = %s, address = %s, 
            role = %s, updated_at = now()
        where id = %s 
        """,
        (
            data['first_name'],
            data['last_name'],
            data['email'],
            data['phone'], 
            data.get('dob') or None, 
            data.get('gender') or None,
            data.get('address') or None,
            data['role'],
            user_id,
        )
    )

 
def update_user_password(user_id, hashed_password):
    """
    Update user password by id. 
    Return True if update is successful, False otherwise.
    """
    
    execute(
        """
        update users  
        set password = %s, updated_at = now()
        where id = %s 
        """,
        (
            hashed_password,
            user_id,
        )
    )
    
    
def delete_user(user_id):
    """
    Delete user by id. 
    Return True if delete is successful, False otherwise.
    """
    try:
        execute('delete from users where id=%s', (user_id,))
        return True
    except Exception as e:
        logger.exception('delete_user failed id=%s: %s', user_id, e)
        return False