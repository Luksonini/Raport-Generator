from django.urls import path
from . import views
# app_name = 'raport_from_list'

urlpatterns = [
    path('upload_docx/<slug:username>/', views.list_upload, name='upload_docx'),
    path('list_upload/<slug:username>/', views.create_replace_list, name='list_upload'),
    path('load_docx_example/<slug:username>/', views.load_example, name='load_example'),
    path('results_page/<slug:username>/', views.results_page, name='results_page'),
]