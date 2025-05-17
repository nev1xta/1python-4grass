from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "app"

urlpatterns = [
    path('login/', views.index),
    path('register/', views.register.as_view(), name='register'),
    path('profile/', views.profile, name="profile"),
    path('profile/<int:file_id>/', views.profile_files),
    # path('download/<str:filename>/', views.download_file, name='download_file'),
    # path('profile/<int:fileid>/', views.files_viewer, name="detail_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)