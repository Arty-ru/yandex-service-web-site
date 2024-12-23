from django.db import models

# Create your models here.

class NiftiStudyTypes(models.Model):
	study_type = models.CharField(max_length=55, default="Aneurysm", verbose_name="Тип исследования")

	@classmethod
	def get_default_pk(cls):
		type, created = cls.objects.get_or_create(
			study_type='default type',
		)
		return type.pk

class NiftiDir(models.Model):
	study_name = models.CharField(verbose_name="Директория")
	study_type = models.ForeignKey('NiftiStudyTypes', on_delete=models.PROTECT, default=NiftiStudyTypes.get_default_pk, null=False)

def content_file_name(instance, filename):
	 return "Dicom/{folder}/{file}".format(folder=NiftiDir.objects.latest('id').study_name, file=filename)

class NiftiFiles(models.Model):
	study_id = models.ForeignKey('NiftiDir', on_delete=models.DO_NOTHING, null=True, verbose_name="ID директории")
	dir = models.FileField(upload_to=content_file_name, verbose_name="Файл")
