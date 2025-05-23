from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from .models import UploadFiles
from django.conf import settings
from django.db import models
from .forms import RegisterForm, UploadFileForm, NewPrivilegedUser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse
import os
from django.contrib import messages


# from .forms import NewUserForm
from django.contrib.auth.decorators import login_required

def index(request):

    return render(request, "registration/login.html")

class register(FormView):
    form_class = RegisterForm

    template_name = "registration/registration.html"
    success_url = reverse_lazy("app:profile")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
def profile_files(request, file_id):
    file = UploadFiles.objects.get(id=file_id)
    User = get_user_model()
    users_with_file = []
    for user in map(int, file.authorized_users.keys()):
        users_with_file.append(User.objects.get(id=user))

    non_signatories = []
    for user in users_with_file:
        if file.authorized_users[str(user.id)] == 1:
            non_signatories.append(user)
    # print(users_with_file)

    if request.method == "POST":
        form_add_user = NewPrivilegedUser(request.POST)
        form_replace_file = UploadFileForm(request.POST, request.FILES)
        if "addUserbutton" in request.POST:
            if form_add_user.is_valid():
                if not (form_add_user.cleaned_data["role"]):
                    messages.success(request, 'роль пользователя не выбрана')
                elif not (User.objects.filter(username=request.POST["user"]).exists()):
                    messages.success(request, 'пользователь не существует')
                else:
                    cd = form_add_user.cleaned_data
                    
                    users = User.objects.get(username=request.POST["user"])
                    file.authorized_users[int(users.id)] = int(cd["role"])
                    file.save()
        if "sign" in request.POST:
            file.authorized_users[int(request.user.id)] = 2
            file.save()
        if "ReplaceFiles_button" in request.POST:
            if form_replace_file.is_valid():
                file.file =  form_replace_file.cleaned_data['file']
                file.save()
        if "comeback" in request.POST:
            return HttpResponseRedirect(reverse("app:profile"))
        if "DeleteFiles_button" in request.POST:
            file.delete_file()
            return HttpResponseRedirect(reverse("app:profile"))


    else:
        form_add_user = NewPrivilegedUser()

    contex = {
        "file" : file,
        "form_add_user" : form_add_user,
        "form_replace_file" : form_replace_file,
        "users" : users_with_file,
        "non_signatories" : non_signatories,
    }
    return render(request, "app/file_temp.html", context=contex)


@login_required
def profile(request):
    all_files = UploadFiles.objects.all()


    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if "UploadFiles_button" in request.POST:
            if form.is_valid():
                authorized_users_data = {
                    request.user.id: 2
                }

                fp = UploadFiles(file=form.cleaned_data['file'], father_user=request.user.id, authorized_users=authorized_users_data)
                fp.save()
            return HttpResponseRedirect(reverse("app:profile"))
    else:
        form = UploadFileForm()
    this_user_files = []
    for file in all_files:
        for key in file.authorized_users.keys():
            if str(request.user.id) == key:
                if file.authorized_users[str(request.user.id)] == 1 or file.authorized_users[str(request.user.id)] == 2:
                    this_user_files.append(file)

    context = {
        # 'all_files': all_files,
        'form': form,
        'this_user_files' : this_user_files,

    }
    return render(request, "app/profile.html", context=context)

