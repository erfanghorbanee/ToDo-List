from django.urls import path
from .views import home, about, delete, cross_off, uncross, edit, register, login_view, get_public_holiday

urlpatterns = [
    path('', login_view, name='login'),
    path('register', register, name='register'),
    path('home', home, name='home'),
    path('about', about, name='about'),
    path('delete/<list_id>', delete, name='delete'),
    path('cross_off/<list_id>', cross_off, name='cross_off'),
    path('uncross/<list_id>', uncross, name='uncross'),
    path('edit/<list_id>', edit, name='edit'),
    path('api/holidays', get_public_holiday, name="holidays"),
    
]
