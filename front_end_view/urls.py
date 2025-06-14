from django.urls import path
from .views import index, login_register, resume_list


urlpatterns = [
path('', index, name='index'),
path('login-register', login_register, name='login-register'),
path('uploaded-resumes', resume_list, name='uploaded-resumes'),
]
