from django.urls import path

from .views import ResumeUploadView, MatchResumeView, RegisterView, UserView, ResumeListView

urlpatterns = [
path('resume/upload/', ResumeUploadView.as_view(), name='resume-upload'),
path('resume/match/', MatchResumeView.as_view(), name='resume-match'),
path('register/', RegisterView.as_view(), name='register'),
path('user-info/', UserView.as_view(), name='user-info'),
path('resume-list/', ResumeListView.as_view(), name= 'resume-list'),
path('resume-list/<int:pk>', ResumeListView.as_view(), name= 'resume-delete')
]
