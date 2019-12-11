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
    participants = forms.CharField(widget=forms.SelectMultiple(attrs={'class': 'form-control choices'}), required=False)
    meet_contents = summer_fields.SummernoteTextFormField(label='', widget=forms.TextInput(), required=False, error_messages={'required': (u'내용을 입력해주세요'), })
    file1 = forms.FileField(label='첨부파일1', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    file2 = forms.FileField(label='첨부파일2', widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = Meeting
        fields = ('meet_date', 'meet_title', 'meet_desc', 'participants', 'meet_contents', 'file1', 'file2')

    def __init__(self, *args, **kwargs):
        super(MeetingAddForm, self).__init__(*args, **kwargs)
        self.fields['file1'].required = False
        self.fields['file2'].required = False


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='내용', widget=forms.Textarea(
        attrs={'class': 'form-control comment-input', 'placeholder': '내용', 'aria-label': '내용'}
    ), required=True)

    class Meta:
        model = Comment
        fields = ('text',)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='계정명',widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter username'}
    ))
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter password'}
    ))


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label='계정명', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter username'}
    ))
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter password'}
    ))
    password2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter password again'}
    ))
    email = forms.EmailField(label='이메일', required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter email address'}
    ))
    nickname = forms.CharField(label='별명', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter display nickname'}
    ))

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email', 'nickname')
