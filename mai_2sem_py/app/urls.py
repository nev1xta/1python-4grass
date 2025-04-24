from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    path('login/', views.index),
    path('register/', views.register.as_view(), name='register'),
    path('profile/', views.profile, name="profile"),
    path('profile/<int:file_id>/', views.profile_files),
    # path('profile/<int:fileid>/', views.files_viewer, name="detail_file"),
]