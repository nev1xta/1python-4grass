from django.contrib.auth.forms import UserCreationForm
from django import forms



class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # self.fields.pop('password1')
        # self.fields.pop('password2')

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", )
        widgets = {
            "email": forms.HiddenInput(),
            "username": forms.HiddenInput(),
        }
        

class NewPrivilegedUser(forms.Form):
    user = forms.IntegerField 

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
    # json = forms.JSONField(ladel="json")