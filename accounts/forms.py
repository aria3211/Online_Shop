from django import forms
from .models import User,OTP
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login') 


class UserRegistreationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField(label='full name')
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone(self):
        cd = self.cleaned_data
        if User.objects.filter(phone_number=cd['phone']).exists():
            raise ValidationError('this phone is already exist')
        OTP.objects.filter(phone_number=cd['phone']).delete()

        return cd['phone']
    def clean_email(self):
        cd = self.cleaned_data['email']
        if User.objects.filter(email=cd).exists():
            raise ValidationError('this email is already exist')
        return cd
    
class VerfyCodeForm(forms.Form):
    code = forms.IntegerField()
    # def clean_code(self):
    #     code = self.cleaned_data['code']
    #     if OTP.objects.filter(code=code).exists():
    #         raise ValidationError('this email is already exist')
    #     return code

class LoginForm(forms.Form):
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)