from django.urls import path

from . import views

urlpatterns = [
    path('list/<int:artist_id>/', views.music_list, name='music-list'),
    path('create/<int:artist_id>/', views.music_create , name='music-create'),
    path('edit/<int:artist_id>/<int:music_id>/', views.music_edit , name='music-edit'),
    path('delete/<int:artist_id>/<int:music_id>/', views.music_delete , name='music-delete'),
    
]