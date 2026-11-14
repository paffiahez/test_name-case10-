from django.urls import path
from . import views

urlpatterns = [
    path('proftests/', views.test_list, name='test_list'),
    path('proftests/<slug:slug>/', views.test_detail, name='test_detail'),
]
