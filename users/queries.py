from core.db import execute

def create_user(data, hashed_password):
    
    user = execute(
        """insert into users 
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