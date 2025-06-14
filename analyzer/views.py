from ast import Mult
from numpy import extract
import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from sklearn.metrics.pairwise import cosine_similarity
from .models import Resume
from .serializers import ResumeSerializer, RegisterSerializer
from django.shortcuts import render
from .utils import extract_text, extract_resume_info, extract_jd_skills
from sentence_transformers import SentenceTransformer
import os

from analyzer import serializers
 
# Create your views here.

class RegisterView(APIView):
  permission_classes = [AllowAny]
  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "User created successfully"}, status=201)
    return Response(serializer.errors, status=400)

class ResumeUploadView(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [MultiPartParser, FormParser]
  ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc']
  ALLOWED_CONTENT_TYPES = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]


  def post(self, request):
    file_obj = request.FILES.get('file')
    if not file_obj:
      return Response({'error': 'No file provided'}, status=400)
    ext = os.path.splitext(file_obj.name)[1].lower()
    if ext not in self.ALLOWED_EXTENSIONS:
      return Response({'error': 'Only Pdf or Word documents are allowed'}, status=400)
    if file_obj.content_type not in self.ALLOWED_CONTENT_TYPES:
      return Response({'error': f'Invalid file type: {file_obj.content_type}'}, status=400)
    
    resume = Resume.objects.create(user=request.user, file = file_obj)
    return Response({
      'message': 'Resume uploaded successfully',
      'resume_id': resume.id
      },status=201)

sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

class MatchResumeView(APIView):
  permission_classes = [IsAuthenticated]
  
  def post(self, request):
    resume_id = request.data.get('resume_id')
    jd_text = request.data.get('job_description', '')
    try:
      resume = Resume.objects.get(id=resume_id, user=request.user)
    except Resume.DoesNotExist:
      return Response({'error': 'Resume not found'}, status=404)
    # Extract resume text
    resume_text = extract_text(resume.file.path)
    resume_info = extract_resume_info(resume_text)
    if 'message' in resume_info:
      return Response({'error': resume_info['message']}, status=400)
    
    resume_skills = set(map(str.lower, resume_info.get('skills', [])))

    jd_skills = set(map(str.lower, extract_jd_skills(jd_text)))

    
    matched_skills = list(resume_skills & jd_skills)
    missing_skills = list(jd_skills - resume_skills)
    # Compute similarity
    resume_emb = sbert_model.encode(resume_text)
    jd_emb = sbert_model.encode(jd_text)
    score = float(cosine_similarity([resume_emb], [jd_emb])[0][0]) * 100
    # (Optional) Extract and compare skills here...
    return Response({
      'compatibility_score': round(score, 2),
      'matched_skills': matched_skills,
      'missing_skills': missing_skills,
      'recommendations': (
        "Include relevant skills from job description to improve match."
        if score < 90 else "Strong match! Resume is well-aligned."
      )
    })

class ResumeListView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    serializer = ResumeSerializer(Resume.objects.filter(user=request.user), many=True)
    return Response(serializer.data)
  def delete(self, request, pk):
    try:
      resume = Resume.objects.get(pk = pk, user = request.user)
      resume.delete()
      return Response({
        'message': 'Resume deleted successfully',        
      }, status=200)
    except Resume.DoesNotExist:
      return Response({'error': 'Resume not found'}, status=404)
    


class UserView(APIView):
  permission_class = [IsAuthenticated]
  
  def get(self, request):
    user = request.user
    return Response({
      'id': user.id,
      'username': user.username,
      'email': user.email,
      'is_staff': user.is_staff,
    })