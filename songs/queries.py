import logging

from core.db import execute
from core.pagination import paginate

logger = logging.getLogger(__name__)


def create_music(data, artist_id): 
    """
    Create a new music record for an artist.
    Returns the created music if successful, None otherwise.
    """
    
    try:
        
        music = execute(
            """
            insert into music
            (artist_id, title, album_name, genre)
            values (%s, %s, %s,%s)
            returning id
            """,
            (
                artist_id,
                data['title'],
                data.get('album_name') or None,
                data.get('genre') or None
            ),
            fetch='one'
        )
        return music
    except Exception as e:
        logger.error(f"Error creating music: {e}")
        return None
    
    
def update_music(music_id, data): 
    """
    Update music by id. 
    Return True if update is successful, False otherwise.
    """
    
    try:
        
        execute(
            """
            update music
            set title=%s, album_name=%s, genre=%s, updated_at=NOW()
            where id=%s
            """,
            (
                data['title'],
                data.get('album_name') or None,
                data.get('genre') or None,
                music_id
                
            )
        )
        
        return True
    
    except Exception as e:
        logger.error(f"Error updating music: {e}")
        return None
    
    
def get_music_page_per_artist(artist_id,page, per_page=10):
    """
    Fetch music data paginated for a specific artist. 
    
    Params: 
        artist_id(int) : id of the artist whose music is to be fetched.
        
        page(int) : current page no requested. 
        
        per_page(int) : no of record per page
        
    Returns:
        Return a dict of pagination metadata
    
    """
    
    try:
        pagination = paginate(
            sql_count='select count(*) as count from music where artist_id=%s',
            sql_data='''
                select id, artist_id, title, genre, album_name, created_at
                from music
                where artist_id =%s
                order BY created_at desc
                limit %s offset %s
            ''',
            params=(artist_id,),
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


def get_music_by_id(music_id):
    """
    Fetch artist by id. Return None if not found.
    """
    
    try:
        return execute(
            'select * from music where id = %s',
            (music_id,), 
            fetch='one'
        )
    except Exception as e:
        logger.exception('get_song_by_id failed id=%s: %s', music_id, e)
        return None

        
def delete_music(music_id):
    """
    Delete music by id. 
    Return True if delete is successful, False otherwise.
    """
    try:
        execute('delete from music where id=%s', (music_id,))
        return True
    except Exception as e:
        logger.exception('delete_music failed id=%s: %s', music_id, e)
        return False