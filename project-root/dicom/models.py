from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class DicomStudyTypes(models.Model):
	study_type = models.CharField(max_length=55, default="Aneurysm", verbose_name="Тип исследования")

	@classmethod
	def get_default_pk(cls):
		type, created = cls.objects.get_or_create(
			study_type='default type', 
		)
		return type.pk

class DicomDirs(models.Model):
	study_name = models.TextField(verbose_name="Директория")
	study_type = models.ForeignKey('DicomStudyTypes', on_delete=models.PROTECT, default=DicomStudyTypes.get_default_pk, null=False)
	screens = ArrayField(models.CharField(max_length=10), verbose_name="Снимки")

def content_file_name(instance, filename): 
	return "Dicom/{folder}/{file}".format(folder=DicomDirs.objects.latest('id').study_name, file=filename)

class DicomFiles(models.Model):
	study_id = models.ForeignKey('DicomDirs', on_delete=models.CASCADE, null=True, verbose_name="ID директории")
	dir = models.FileField(upload_to=content_file_name, verbose_name="Файл")

class DicomUpdates(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="ID пользователя")
	dir = models.ForeignKey('DicomDirs', on_delete=models.RESTRICT, verbose_name="ID директории")
	date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
