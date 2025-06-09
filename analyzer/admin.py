from django.contrib import admin

# Register your models here.
from .models import Resume


class ResumeAdmin(admin.ModelAdmin):
  list_display = ('file_name', 'uploaded_by')

  def file_name(self, obj):
    return obj.file.name.split('/')[-1]
  file_name.short_description = 'Resume File Name'

  def uploaded_by(self, obj):
    return obj.user.username
  uploaded_by.short_description = 'Uploaded By'


admin.site.register(Resume, ResumeAdmin)
