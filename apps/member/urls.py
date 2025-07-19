from django.urls import path
from .views import ProfileView
from apps.member.views import BorrowBookView, ReturnBookView

urlpatterns = [
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('borrow/', BorrowBookView.as_view(), name='borrow'),
    path('return/', ReturnBookView.as_view(), name='return'),
]
