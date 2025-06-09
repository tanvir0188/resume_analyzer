from django.urls import path
from .views import index, login_register


urlpatterns = [
path('', index, name='index'),
path('login-register', login_register, name='login-register'),
]
