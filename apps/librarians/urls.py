from django.urls import path
from .views import AddBookView , edit_book, delete_book, AllProfilesView

urlpatterns = [
    path('all-profiles/', AllProfilesView.as_view(), name='all_profiles'),
    path('add/', AddBookView.as_view(), name='add_book'),
    path('edit/<int:book_id>/', edit_book, name='edit_book'),
    path('delete/<int:book_id>/', delete_book, name='delete_book'),
    
]
