from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.forms import UserCreationForm
from .models import UploadFiles
from django.db import models
from .forms import RegisterForm, UploadFileForm, NewPrivilegedUser
from django.contrib.auth import get_user_model

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
    if request.method == "POST":
        form = NewPrivilegedUser(request.POST)
        if "addUserbutton" in request.POST:
            if form.is_valid():
                cd = form.cleaned_data
                
                users = User.objects.get(username=request.POST["user"])
                file.authorized_users[int(users.id)] = int(cd["role"])
                file.save()
        if "comeback" in request.POST:
            return HttpResponseRedirect(reverse("app:profile"))
    else:
        form = NewPrivilegedUser()

    contex = {
        "file" : file,
        "form" : form
    }
    return render(request, "app/file_temp.html", context=contex)

@login_required
def profile(request):
    all_files = UploadFiles.objects.all()


    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if "UploadFiles_button" in request.POST:
            if form.is_valid():
                print(request.POST)
                # handle_uploded_file(form.cleaned_data['file'])
                authorized_users_data = {
                    request.user.id: 1
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

