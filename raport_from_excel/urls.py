from django.urls import path
from . import views

# app_name = 'raport_from_excel'

urlpatterns = [
    path('upload_excel/<slug:username>/', views.excel_upload, name='upload_excel'),
    path('choose_columns/<slug:username>/', views.choose_columns, name='choose_columns'),
    path('load_excel_example/<slug:username>/', views.load_excel_example, name='load_excel_example'),
]
    