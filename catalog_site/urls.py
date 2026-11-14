from django.contrib import admin
from django.urls import path
from catalog.views import home, about, contacts, login_view, profile_view, send_message, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('send_message/', send_message, name='send_message'),
    path('logout/', logout_view, name='logout'),
]