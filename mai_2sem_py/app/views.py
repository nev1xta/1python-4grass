from django.shortcuts import render
from django.http import HttpResponse
from .models import Files

def index(request):
    return render(request, "app/index.html")

def register(request):
    return render(request, "app/registration.html")


def profile(request):
    all_files = Files.objects.all()
    current_files = {
        "files": all_files
    }
    return render(request, "app/profile.html", current_files)


def files_viewer(request, fileid):
    return HttpResponse("app/profile.html")