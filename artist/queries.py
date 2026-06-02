import logging

from core.db import execute
from core.pagination import paginate

logger = logging.getLogger(__name__)


def create_artist(data):
    """
    Create a new artist record.
    Returns the created artist if successful, None otherwise.
    """
    

    try:
        artist = execute(
            """
                insert into artist
                (name, dob, gender, address, first_release_year, no_of_albums_released)
                values (%s, %s, %s, %s, %s, %s)
                returning id
            """,
            (
                data['name'],
                data.get('dob') or None,
                data.get('gender') or None,
                data.get('address') or None,
                data.get('first_release_year') or None,
                data.get('no_of_albums_released') or 0,
            ),
            fetch='one'
        )
        
        return artist
    
    except Exception as e:
        logger.error(f"Error creating artist: {e}")
        return None


def update_artist(artist_id, data):
    """
    Update artist by id. 
    Return True if update is successful, False otherwise.
    """
    try:
        execute("""
            update artist
            set name=%s, dob=%s, gender=%s, address=%s,
                first_release_year=%s, no_of_albums_released=%s,
                updated_at=NOW()
            where id=%s
        """, (
            data['name'],
            data.get('dob') or None,
            data.get('gender') or None,
            data.get('address') or None,
            data.get('first_release_year') or None,
            data.get('no_of_albums_released') or 0,
            artist_id,
        ))
        return True
    except Exception as e:
        logger.exception('update_artist failed id=%s: %s', artist_id, e)
        return False
    
    
def get_artists_page(page, per_page=10):
    """
    Fetch artist data paginated. 
    
    Params: 
        page(int) : current page no requested. 
        
        per_page(int) : no of record per page
        
    Returns:
        Return a dict of pagination metadata
    
    """
    
    try:
        pagination = paginate(
            sql_count='select count(*) as count from artist',
            sql_data='''
                select id, name, dob, gender, address,
                       first_release_year, no_of_albums_released, created_at
                from artist
                order BY created_at desc
                limit %s offset %s
            ''',
            params=(),
            page=page,
            per_page=per_page,
        )
        return pagination
    
    except Exception as e:
        logger.exception('Pagination failed for get_artist_page: %s', e)
        return {
            'rows':        [],
            'page':        1,
            'per_page':    per_page,
            'total':       0,
            'total_pages': 1,
            'has_prev':    False,
            'has_next':    False,
            'page_range':  range(1, 2),
            'error':       True,
        }
 
        
def get_artist_by_id(artist_id):
    """
    Fetch artist by id. Return None if not found.
    """
    
    try:
        artist = execute(
            'select * from artist where id = %s',
            (artist_id,), fetch='one'
        ) 
        return artist
    
    except Exception as e:
        logger.exception('get_artist_by_id failed id=%s: %s', artist_id, e)
        return None
   
    
def delete_artist(artist_id):
    """
    Delete artist by id. 
    Return True if delete is successful, False otherwise.
    """
    try:
        execute('delete from artist where id=%s', (artist_id,))
        return True
    except Exception as e:
        logger.exception('delete_artist failed id=%s: %s', artist_id, e)
        return False