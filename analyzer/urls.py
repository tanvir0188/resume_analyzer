from django.urls import path

from .views import ResumeUploadView, MatchResumeView, RegisterView, UserView

urlpatterns = [
path('resume/upload/', ResumeUploadView.as_view(), name='resume-upload'),
path('resume/match/', MatchResumeView.as_view(), name='resume-match'),
path('register/', RegisterView.as_view(), name='register'),
path('user-info/', UserView.as_view(), name='user-info'),
]
