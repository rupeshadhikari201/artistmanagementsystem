from core.db import execute

def user_register(data, hashed_password):
    """"
    Register a new user.
    On Success return the user else None
    """
    
    user = execute(
        """insert into users 
            (first_name, last_name, email, password, phone, role )
            values (%s, %s, %s, %s, %s, %s)
        """,
        (
            data['first_name'],
            data['last_name'],
            data['email'],
            hashed_password,
            data['phone'],
            data['role'],
        )
  
    )
    
    return user   