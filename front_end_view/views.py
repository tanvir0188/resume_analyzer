from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'index.html')

def login_register(request):
  return render(request, 'login-register.html')

def resume_list(request):
  return render(request, 'resume-list.html')