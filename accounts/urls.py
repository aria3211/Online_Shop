from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='user_register'),
    path('verfycode/',views.VerfyCodeView.as_view(),name='user_verfy'),
    path('login/',views.LoginView.as_view(),name='user_login'),
    path('logout/',views.LogoutView.as_view(),name='user_logout'),
]

