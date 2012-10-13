# -*- coding: utf8 -*- 

from django import forms
from django.core import validators
from django.contrib.auth.models import User

class Signup(forms.ModelForm) :
    email = forms.EmailField(label=u'邮箱', required=True, validators=[validators.validate_email])
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
            raise forms.ValidationError(u'两次输入的密码不相同')
        return confirm_password
    
    def save(self, commit=True) :
        user = super(Signup, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit : user.save()
        return user

