# Register your models here.

from django.contrib import admin
from .models import DicomDirs, DicomUpdates, DicomStudyTypes

class AdminDicomDirs(admin.ModelAdmin):
	list_display = ('id','study_name', 'screens')

class AdminDicomUpdates(admin.ModelAdmin):
	list_display = ('id', 'user', 'dir', 'date')

class AdminDicomStudyTypes(admin.ModelAdmin):
	list_display = ('id', 'study_type')

admin.site.register(DicomDirs, AdminDicomDirs)
admin.site.register(DicomUpdates, AdminDicomUpdates)
admin.site.register(DicomStudyTypes, AdminDicomStudyTypes)
