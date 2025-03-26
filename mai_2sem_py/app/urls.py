from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    path('hello/', views.index),
    path('register/', views.register),
    path('profile/', views.profile),
    path('profile/<int:fileid>/', views.files_viewer, name="detail_file"),
]