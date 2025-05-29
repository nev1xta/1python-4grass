from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from .models import UploadFiles, UpdateNotifications
from django.conf import settings
from django.db import models
from .forms import RegisterForm, UploadFileForm, NewPrivilegedUser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse
import os
from django.contrib import messages
from .forms import SurveyForm
from .sorts import sings, non_sings, names, full_sings, uploadFiles, by_date
import datetime

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
        if file.authorized_users[str(user.id)] == 2:
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
                    file.authorized_users[str(users.id)] = int(cd["role"])
                    file.last_changes_date = datetime.datetime.now()
                    file.save()
                    if int(cd["role"]) == 1:
                        notification = UpdateNotifications(recipient=users.id, text=f"Вы получили доступ к просмотру нового файла: {file.file.name}")
                    elif int(cd["role"]) == 2:
                        notification = UpdateNotifications(recipient=int(users.id), text=f"Вы получили доступ к подписанию нового файла: {file.file.name}")
                    notification.save()
        if "sign" in request.POST:
            file.authorized_users[str(request.user.id)] = 3
            file.last_changes_date = datetime.datetime.now()
            file.save()
            notification = UpdateNotifications(recipient=int(file.father_user), text=f"{ User.objects.get(id=request.user.id).username} подписал файл: {file.file.name}")
            notification.save()
        if "ReplaceFiles_button" in request.POST:
            if form_replace_file.is_valid():
                file.file =  form_replace_file.cleaned_data['file']
                for i in file.authorized_users:
                    if file.authorized_users[i] == 3:
                        file.authorized_users[i] = 2
                    notification = UpdateNotifications(recipient=int(i), text=f"{ User.objects.get(id=request.user.id).username} изменил файл: {file.file.name}")
                    notification.save()
                file.last_changes_date = datetime.datetime.now()
                file.save()
        if "comeback" in request.POST:
            return HttpResponseRedirect(reverse("app:profile"))
        if "DeleteFiles_button" in request.POST:
            for i in file.authorized_users:
                notification = UpdateNotifications(recipient=int(i), text=f"{ User.objects.get(id=request.user.id).username} удалил файл: {file.file.name}")
                notification.save()
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

def notifications(request):
    notifications_to_this_user = UpdateNotifications.objects.filter(recipient=request.user.id)

    if request.method == "POST":
        if "comeback" in request.POST:
            return HttpResponseRedirect(reverse("app:profile"))
        if "delete_notification" in request.POST:
            
            UpdateNotifications.objects.filter(id=int(request.POST["delete_notification"])).delete()
    contex = {
        "notifications_to_this_user" : notifications_to_this_user,
    }

    return render(request, "app/notifications.html", context=contex)

@login_required
def profile(request):
    all_files = UploadFiles.objects.all()

    this_user_files = []
    for file in all_files:
        for key in file.authorized_users.keys():
            if str(request.user.id) == key:
                statuses = [1, 2, 3]
                if file.authorized_users[str(request.user.id)] in statuses:
                    this_user_files.append(file)

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        
        form1 = SurveyForm(request.POST)
        if "filther" in request.POST:
            if form1.is_valid():
                age_group = form1.cleaned_data['age_group']
                print(age_group)
                if age_group == "Подписанные":
                    this_user_files = sings(this_user_files, request.user.id)
                elif age_group == "Не подписанны":
                    this_user_files = non_sings(this_user_files, request.user.id)
                elif age_group == "По имени":
                    this_user_files = names(this_user_files, request.user.id)
                elif age_group == "Завершён":
                    this_user_files = full_sings(this_user_files, request.user.id)
                elif age_group == "Загруженные":
                    this_user_files = uploadFiles(this_user_files, request.user.id)
                elif age_group == "Дата":
                    this_user_files = by_date(this_user_files, request.user.id)
                    
        # if 

        if "UploadFiles_button" in request.POST:
            if form.is_valid():
                if form.cleaned_data['file']:
                    authorized_users_data = {
                        request.user.id: 1
                    }
                    fp = UploadFiles(file=form.cleaned_data['file'], father_user=request.user.id, authorized_users=authorized_users_data, last_changes_date=datetime.datetime.now())
                    fp.save()
                    
                    return HttpResponseRedirect(reverse("app:profile"))
    else:
        form1 = SurveyForm()
        form = UploadFileForm()

    context = {
        # 'all_files': all_files,
        'form': form,
        'form1': form1,
        'this_user_files' : this_user_files,

    }
    return render(request, "app/profile.html", context=context)

