from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process_files, name='process_files'),
    path('result/', views.show_result, name='show_result'),
]