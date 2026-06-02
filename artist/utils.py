import csv
import io
import logging
from datetime import date

logger = logging.getLogger(__name__)

EXPORT_COLUMNS = [
    'name',
    'dob',
    'gender',
    'address',
    'first_release_year',
    'no_of_albums_released',
]

current_year = date.today().year


def parser_artists_csv(file):
    """ 
    Reads the uploaded csv file object.
    
    Returns:
        valid_rows (list)   : cleaned dict to be inserted in db
        skipped_rows (list) : dict 
    """
    
    valid_rows = []
    skipped_rows = []
    
    try:
        decoded = file.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(decoded))
    except Exception as e:
        logger.exception('CSV decode failed : %s', e)
        return [], [{'row': 'file', 'reason' : 'Could not read file. Make sure it is a valid UTF-8 csv.'}]

    # loop each row (skipping the header)
    for i, row in enumerate(reader, start= 2):
        
        # 1. name
        name = row.get('name', '').strip()
        
        if not name:
            skipped_rows.append({'row' : i, 'reason': 'Missing name'})
            continue
        
        # 2. dob
        dob = row.get('dob', '').strip() or None
        
        # 3. gender
        gender = row.get('gender', '').strip().lower()
        if gender not in ('m','f','o',''):
            gender = None
            
        # 4. address
        address = row.get('address', '').strip() or None 


        # 5. first release year
        raw_year = row.get('first_release_year','').strip()
        first_release_year = None
        if raw_year:
            try:
                first_release_year = int(raw_year)
                if not (1900 <= first_release_year <= current_year):
                    skipped_rows.append({
                        'row':    i,
                        'reason': f'first_release_year {first_release_year} out of range (1900–{current_year})'
                    })
                    continue
                
            except ValueError:
                skipped_rows.append({'row' : i, 'reason' : 'Invalid first_release_year'} )
                continue
        
        # 6. no of albums released
        raw_albums = row.get('no_of_albums_released', '').strip()
        try:
            no_of_albums_released = int(raw_albums) if raw_albums else 0
            if no_of_albums_released < 0:
                no_of_albums_released = 0
        except ValueError:
            no_of_albums_released = 0
            
            
        valid_rows.append({
            'name' : name,
            'dob' : dob,
            'gender' : gender or None,
            'address' : address,
            'first_release_year' : first_release_year,
            'no_of_albums_released' : no_of_albums_released
        })
    
    
    return valid_rows, skipped_rows
        

def export_artists_csv(rows):
    pass
    