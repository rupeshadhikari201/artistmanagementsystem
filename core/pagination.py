from core.db import execute

def paginate(sql_count, sql_data, params, page, per_page=10):
    """
        sql_count : sql query to return total no of rows
        sql_data  : sql query to fetch the actual rows with limit and offset
        params    : tuple of parameters to be passed to both sql_count and sql_data for filtering
        page      : the current page number requested by the client
        per_page  : how many records to return per page
    """
    
    total_row = execute(sql_count, params, fetch='one')
    total = total_row['count'] if total_row and 'count' in total_row else 0
    total_pages = max(1, (total + per_page -1) // per_page)
    page = max(1, min(page, total_pages))
    offset = (page -1) * per_page
    
    rows = execute(sql_data, params + (per_page, offset), fetch='all')
    
    return {
        'rows' : rows, 
        'page' : page, 
        'per_page' : per_page,
        'total' : total,
        'total_pages' : total_pages,
        'has_prev' : page > 1,
        'has_next' : page < total_pages,
        'page_range': range(1, total_pages + 1),
    }