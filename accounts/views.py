from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistreationForm,VerfyCodeForm,LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import send_sms 
from .models import OTP,User
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import datetime
import pytz



class RegisterView(View):
    form_class = UserRegistreationForm
    def get(self,request):
        form = self.form_class
        return render(request,'accounts/register.html',{'form':form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            otp = OTP.objects.filter(phone_number=form.cleaned_data['phone']).exists()
            if otp:
                code=OTP.objects.get(phone_number=form.cleaned_data['phone'])
                code.delete()
            code=random.randint(1000,9999)
            send_sms(form.cleaned_data['phone'],code        )
            OTP.objects.create(phone_number=form.cleaned_data['phone'],code=code)
            request.session['user_session'] = {
                'phone_number':form.cleaned_data['phone'],
                'email':form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
				'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:user_verfy')
        return render(request,'accounts/register.html',{'form':form})
           
        

class VerfyCodeView(View):
    form_class = VerfyCodeForm
    template_name = 'accounts/verify.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    def post(self,request):
        user_session = request.session['user_session']
        code_instance = OTP.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            current_time = datetime.datetime.now(tz=pytz.timezone('Asia/Tehran'))
            expire_time = code_instance.created + timedelta(minutes=2)
            print(code_instance)
            if cd['code'] == code_instance.code:
                if  current_time>expire_time:
                    messages.error(request, 'this code is expired please try again', 'danger')
                    code_instance.delete()
                else:  
                    User.objects.create_user(user_session['phone_number'],user_session['email'],user_session['full_name'],user_session['password'])
                    code_instance.delete()
                    messages.success(request, 'you registered.', 'success')
                    return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:user_verfy')
        messages.error(request,'somthing went wrong!!!!','danger')
        return redirect('accounts:user_register')
    

class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    def setup(self, request, *args, **kwargs) -> None:
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    
    def get(self,request):
        return render(request,self.template_name,{'form':self.form_class})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phone_number=cd['phone'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request, 'you logged in successfully', 'info')
                
                if self.next:
                    return redirect(self.next)
                
                return redirect('home:home')
            messages.error(request, 'phone or password is wrong', 'warning')
        return render(request, self.template_name, {'form':form})

class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')
    