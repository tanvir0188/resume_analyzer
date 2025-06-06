from django.urls import path

from .views import ResumeUploadView, MatchResumeView, RegisterView

urlpatterns = [
path('resume/upload/', ResumeUploadView.as_view(), name='resume-upload'),
path('resume/match/', MatchResumeView.as_view(), name='resume-match'),
path('register/', RegisterView.as_view(), name='register'),
]
