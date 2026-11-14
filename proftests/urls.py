from django.urls import path
from . import views

urlpatterns = [
    path('proftests/', views.test_detail, name='proftests'),
]
