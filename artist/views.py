import logging
import csv
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render,redirect

from .queries import (
    create_artist,
    get_artists_page,
    get_artist_by_id,
    update_artist,
    delete_artist,
    bulk_insert_artists
)
from .utils import (
    parser_artists_csv
)
from .forms import (
    ArtistCreateForm,
    ArtistEditForm,
    ArtistImportForm
)
logger = logging.getLogger(__name__)


def artist_list(request):
    
    try:
        page = int(request.GET.get('page', 1))
        data = get_artists_page(page, per_page=5)
        
        return render(
            request, 
            'artist/list.html',
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
                'rows': [],
                'error': 'Something went wrong. Please try again later.',
            }
        )
    except Exception as e:
        logger.exception("Artist list failed")
        return render(
            request, 
            'artist/list.html', {
                'rows': [],
                'error': 'Something went wrong. Please try again later.',
            }
        )
        
        
def artist_create(request):
    
    if request.method == 'POST':
        form = ArtistCreateForm(request.POST)
        
        if form.is_valid():
            
            data = form.cleaned_data
            
            try:
                artist = create_artist(data)
                
                if artist:
                    logger.info(f"Artist created successfully.")
                    return redirect('artist-list')
                else:
                    logger.warning("Artist creation failed")
                    form.add_error(None, "Failed to create artist. Please try again.")
            
            except Exception as e:
                logger.exception("Artist creation failed")
                form.add_error(None, "Something went wrong. Please try again later.")  
    
    else:
        form = ArtistCreateForm()

    return render(
        request, 
        'artist/create.html',
        {
            'form' : form,
        }
    )


def artist_edit(request, artist_id):
    
    target = get_artist_by_id(artist_id)
    
    if not target:
        logger.warning(f"Artist not found for id: {artist_id}")
        return redirect('artist-list')
    
    if request.method == 'POST':
        
        form = ArtistEditForm(request.POST)
        
        if form.is_valid():
            
            data = form.cleaned_data
            
            try:
                success = update_artist(artist_id, data)
                
                if success:
                    logger.info(f"Artist updated successfully for id: {artist_id}")
                    return redirect('artist-list')
                else:
                    logger.warning(f"Artist update failed for id: {artist_id}")
                    form.add_error(None, "Failed to update artist. Please try again.")
            
            except Exception as e:
                logger.exception(f"Artist update failed for id: {artist_id}")
                form.add_error(None, "Something went wrong. Please try again later.")
        
    else:
        form = ArtistEditForm(
            initial={
                k: target.get(k, '') for k in ArtistEditForm.base_fields.keys()
            }
        )

    return render(
        request, 
        'artist/edit.html',
        {
            'form': form,
            'target': target,
        }
    )


def artist_delete(request, artist_id):  
    
    if request.method == 'POST':
        
        try:
            target = get_artist_by_id(artist_id)
            
            if target:
                delete_artist(artist_id)
                logger.info(f"Artist deleted successfully for id: {artist_id}")
            else:
                logger.warning(f"Artist not found for deletion with id: {artist_id}")
        except Exception as e:
            logger.exception(f"Artist deletion failed for id: {artist_id}") 
            
    return redirect('artist-list')


def artist_import(request):
    
    if request.method == 'POST':
        
        form = ArtistImportForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            file = form.cleaned_data['file']
            
            # parse file 
            valid_rows, skipped_rows = parser_artists_csv(file)
            
            print(valid_rows)
            
            if not valid_rows and not skipped_rows:
                logger.error('file', 'CSV has no readable rows. Check the format.')
                form.add_error('file', 'CSV has no readable rows. Check the format.')
                
            # insert to db
            inserted = 0
            if valid_rows:
                
                try:
                    inserted = bulk_insert_artists(valid_rows)
                    logger.info(
                        'Bulk import done. Inserted = %s, Skipped = %s by user=%s',
                        inserted, len(skipped_rows), request.session['user']['id']
                        )
                    
                    return redirect('artist-list')
                    
                except Exception as e:
                    logger.exception('Bulk Insert failed: %s', e)
                    form.add_error(None, 'Database error. No records were saved. Please try again.')
                    
            else:
                logger.error('No Valid rows.')
                form.add_error(None, 'No valid rows.')
            
    else:
        form = ArtistImportForm()

    return render(
        request, 
        'artist/import.html', 
        {
            'form':         form,
            'user':         request.session.get('user'),
            'current_year': date.today().year,
        }
    )
    
def download_artist_sample_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="artist_sample.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'name',
        'dob',
        'gender',
        'address',
        'first_release_year',
        'no_of_albums_released'
    ])

    writer.writerow(['Ram', '1988-05-05', 'f', 'London', 2008, 4])
    writer.writerow(['Shyam', '1986-10-24', 'm', 'Toronto', 2010, 7])

    return response