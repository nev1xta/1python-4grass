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
    # role = forms.RadioSelect

    CHOICES = [
        ('1', 'читатель'),
        ('2', 'на подпись'),
        
    ]
    role = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES, required=False
    )

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл", required=False)
    # json = forms.JSONField(ladel="json")



class SurveyForm(forms.Form):
    # Статические варианты выбора
    AGE_GROUP_CHOICES = [
        ('', '--- Выберите возрастную группу ---'),  # Пустой вариант
        ('Дата', 'По дате последнего именения'),
        ('Подписанные', 'Подписанные'),
        ('Не подписанны', 'Не подписанные'),
        ('По имени', 'По имени'),
        ('Завершён', 'Завершёные'),
        ('Загруженные', 'Загруженные'),
    ]
    
    # Выпадающий список (основное поле)
    age_group = forms.ChoiceField(
        label="Возрастная группа",
        choices=AGE_GROUP_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'age-group-select'
        }),
        required=False  # Обязательное поле
    )
    
    # Динамические choices можно установить в __init__
    def __init__(self, *args, **kwargs):
        dynamic_choices = kwargs.pop('dynamic_choices', None)
        super(SurveyForm, self).__init__(*args, **kwargs)
        
        if dynamic_choices:
            self.fields['age_group'].choices = dynamic_choices

# class delete_notification(forms.Form):
#     delete = forms.