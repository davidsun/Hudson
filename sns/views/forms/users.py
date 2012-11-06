# -*- coding: utf8 -*- 

from django import forms
from django.core import validators
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class Login(forms.Form) :
    email = forms.EmailField(label=u'邮箱', required=True)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput, required=True, min_length=6, max_length=30)

    def clean(self) :
        email = self.cleaned_data.get("email", "")
        password = self.cleaned_data.get("password")
        if authenticate(email=email, password=password) is None : raise validators.ValidationError(u'您输入的邮箱或密码不正确。')
        return self.cleaned_data
    
    def save(self, request) :
        email = self.cleaned_data.get("email", "")
        password = self.cleaned_data.get("password", "")
        user = authenticate(email=email, password=password)
        login(request, user)
        return user

class Signup(forms.ModelForm) :
    email = forms.EmailField(label=u'邮箱', required=True)
    username = forms.CharField(label=u'用户名', required=True, min_length=1, max_length=30)
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput, required=True, min_length=6, max_length=30)
    confirm_password = forms.CharField(label=u'重复密码', widget=forms.PasswordInput, required=True) 

    class Meta :
        model = User
        fields = ("email", "username")

    def clean_username(self) :
        username = self.cleaned_data.get("username", "")
        try :
            User.objects.get(username=username)
        except User.DoesNotExist :
            return username
        raise validators.ValidationError(u'抱歉，用户名 %s 已被使用。' % username)

    def clean_email(self) :
        email = self.cleaned_data.get("email", "")
        try :
            User.objects.get(email=email)
        except User.DoesNotExist :
            return email
        raise validators.ValidationError(u'邮箱 %s 已被注册。' % email)
    
    def clean_confirm_password(self) :
        password = self.cleaned_data.get("password", "")
        confirm_password = self.cleaned_data.get("confirm_password", "")
        if password != confirm_password:
            raise forms.ValidationError(u'两次输入的密码不相同。')
        return confirm_password
    
    def save(self, commit=True) :
        user = super(Signup, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit : user.save()
        return user

# How django forms anti-human is !!!
class Edit(forms.Form):
    old_password = forms.CharField(label=u'旧密码', widget=forms.PasswordInput, required=True)
    username = forms.CharField(label=u'用户名', min_length=1, max_length=30, required=False)
    password = forms.CharField(label=u'新密码', widget=forms.PasswordInput, min_length=6, max_length=30, required=False)
    confirm_password = forms.CharField(label=u'重复密码', widget=forms.PasswordInput, required=False) 

    def __init__(self, user=None, *args, **kwargs):
        super(Edit, self).__init__(*args, **kwargs)
        self._user = user

    def clean_username(self) :
        username = self.cleaned_data.get("username", "")
        if not username: return username
        try :
            User.objects.get(username=username)
        except User.DoesNotExist :
            return username
        raise validators.ValidationError(u'抱歉，用户名 %s 已被使用。' % username)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password", "")
        if not self._user.check_password(old_password):
            raise validators.ValidationError(u'您输入的或密码不正确。')
        return old_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password", "")
        confirm_password = self.cleaned_data.get("confirm_password", "")
        if password != confirm_password:
            raise forms.ValidationError(u'两次输入的密码不相同。')
        return confirm_password

    def save(self):
        password = self.cleaned_data.get("password", "")
        username = self.cleaned_data.get("username", "")
        if password:
            self._user.set_password(self.cleaned_data["password"])
        if username:
            self._user.username = username
        self._user.save()
        return self._user

