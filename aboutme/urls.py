from django.urls import path
from . import views

# app_name = 'aboutme'

urlpatterns = [ 
    path('aboutme/', views.aboutme, name='aboutme')
]

