from django.urls import path
from . import views

urlpatterns = [
    path('proftests/', views.main, name='proftests'),
]
