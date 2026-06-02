from core.db import execute

def get_dashboard_stats():
    
    stats = {}
    
    # total songs
    stats['total_songs'] = ( execute(
            """ 
            select count(*) as count from music
            """,
            fetch='one') or {}
        ).get('count',0)
    
    
    # total artists 
    stats['total_artists'] = ( execute(
            """ 
            select count(*) as count from artist 
            """, 
            fetch='one') or {}
        ).get('count',0)
    
    
    # total users 
    stats['total_users'] = ( execute(
            """ 
            select count(*) as count from users 
            """, 
            fetch='one') or {}
        ).get('count',0)
    
    
    # genre breakdown
    stats['genre_breakdown'] = execute(
        """ 
        select genre, count(*) as count from music
        where genre is not null 
        group by genre
        order by count desc
        """,
        fetch='all' or []
    )
    
    return stats