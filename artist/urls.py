from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.artist_list, name='artist-list'),
    path('create/', views.artist_create , name='artist-create'),
    path('edit/<int:artist_id>/', views.artist_edit , name='artist-edit'),
    path('delete/<int:artist_id>/', views.artist_delete , name='artist-delete'),
    
]