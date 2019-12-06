from django import forms
from django.contrib.auth import get_user_model

from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from flatpickr import DateTimePickerInput


class MeetingAddForm(forms.ModelForm):
    meet_date = forms.DateTimeField(widget=DateTimePickerInput(options={
        'dateFormat': 'Y-m-d H:i',
    }))
    meet_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    meet_desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                                    'style': 'height: 100px; min-height: 100px;'
                                                                             'max-height: 200px;'}))
    participants = forms.CharField(widget=forms.SelectMultiple(attrs={'class': 'form-control choices'}))

    class Meta:
        model = Meeting
        fields = ('meet_date', 'meet_title', 'meet_desc', 'participants')

    def __init__(self, *args, **kwargs):
        super(MeetingAddForm, self).__init__(*args, **kwargs)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='계정명', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='계정명', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='이메일', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(label='별명', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email', 'nickname')
