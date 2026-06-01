from django.urls import path

from . import views

urlpatterns = [
    path('list', views.user_list, name='users-list'),
    path('create', views.user_create , name='user-create'),
    path('edit/<int:user_id>/', views.user_edit , name='user-edit'),
    path('delete/<int:user_id>/', views.user_delete , name='user-delete'),
    
]
