import logging
from django.contrib import messages
from django.shortcuts import render,redirect

from .queries import (
    create_music,
    get_music_page_per_artist,
    update_music,
    delete_music,
    get_music_by_id
)
from .forms import MusicCreateForm, MusicEditForm
from artist.queries import get_artist_by_id
logger = logging.getLogger(__name__)


def music_list(request, artist_id):
    
    artist = get_artist_by_id(artist_id)
    
    if not artist:
        logger.warning('Artist not found.')
        return redirect('artist-list')
    
    try:
        page = int(request.GET.get('page', 1))
        data = get_music_page_per_artist(artist_id,page)
        
        return render(
            request, 
            'songs/list.html', 
            {
                **data,
                'artist':  artist,
                'offset':  (data['page'] - 1) * data['per_page'],
                'user':    request.session.get('user'),
            }
        )

    
    except ValueError as e:
        logger.warning(f"Invalid page value : {e}")
        return render(
            request, 
            'songs/list.html', 
            {
                'rows': [],
                'error': 'Something went wrong. Please try again later.',
            }
        )
        
    except Exception as e:
        logger.exception("Artist list failed")
        return render(
            request, 
            'songs/list.html', {
                'rows': [],
                'error': 'Something went wrong. Please try again later.',
            }
        )
        

def music_create(request, artist_id):
    
    artist = get_artist_by_id(artist_id)
    if not artist:
        logger.warning(request, 'Artist not found.')
        return redirect('artist-list')
    
    if request.method == 'POST':
        
        form = MusicCreateForm(request.POST)
        
        if form.is_valid():
            
            data = form.cleaned_data
            
            try:
                
                music = create_music(data, artist_id)
                
                if music:
                    messages.success(request, "Music created successfully.")
                    logger.info("Music created successfully.")
                    return redirect('music-list', artist_id=artist_id)
                else:
                    messages.error(request, "Error creating Music")
                    logger.warning("Music Creation failed")
                    form.add_error(None, "Failed to create Music.")
            
            except Exception as e:
                messages.error(request, "Music Creation Failed")
                logger.warning("Music Creation Failed")
                form.add_error(None, "Something went wrong. Please try again later.")  
                
    else:
        form = MusicCreateForm()
            
    return render(
        request, 
        'songs/create.html',
        {
            'form' : form,
            'artist' : artist
        }
    )
      
        
def music_edit(request, artist_id, music_id):
    
    artist = get_artist_by_id(artist_id)
    if not artist:
        logging.error(request, 'Artist not found.')
        return redirect('artist-list')

    music = get_music_by_id(music_id)
    if not music or music['artist_id'] != artist_id:
        logging.error(request, 'Song not found.')
        return redirect('song-list', artist_id=artist_id)
    
    if request.method == 'POST':
        
        form = MusicEditForm(request.POST)
        
        if form.is_valid():
            
            data = form.cleaned_data
            
            try:
                success = update_music(music_id, data)
                
                if success:
                    messages.success(request, "Music updated successfully.")
                    logger.info(f"Music updated successfully for id : {music_id}")
                    return redirect('music-list', artist_id=artist_id)
                
                else:
                    messages.error(request, "Error updating music.")
                    logger.warning(f"Music update failed for id: {music_id}")
                    form.add_error(None, "Failed to update music. Please try again.")
            
            except Exception as e:
                messages.error(request, "Something went wrong.")
                logger.exception(f"Music update failed for id: {music_id}")
                form.add_error(None, "Something went wrong. Please try again later.")
    else:
        form = MusicEditForm(
            initial = {
                k : music.get(k, '') for k in MusicEditForm.base_fields.keys()
            }
        )
        
    return render(
        request, 
        'songs/edit.html',  
        {
            'form': form,
            'music': music,
            'artist' : artist
        }
    )
    
    
def music_delete(request, artist_id, music_id):
    
    if request.method == 'POST':
        
        try:
            music = get_music_by_id(music_id)
            
            if music and music['artist_id'] == artist_id:
                success = delete_music(music_id)
                
                if success:
                    messages.success(request, 'Music deleted successfully.')
                    logger.info(f"Music deleted successfully for id: {music_id}")
                
                else:
                    messages.error(request, 'Error Deleting Music.')
                    logger.error('Failed to delete song.')
            else:
                logger.warning(f"Music not found for deletion with id: {music_id}")
        
        except Exception as e:
            logger.exception(f"Music deletion failed for id: {music_id}") 
            
    return redirect('music-list', artist_id=artist_id)