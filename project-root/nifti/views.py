from django.shortcuts import render, redirect
from webapp.settings import MEDIA_ROOT
from dicom.models import DicomDirs
from .models import NiftiDir, NiftiFiles
import os
from pathlib import Path
import dicom2nifti
import dicom2nifti.settings as settings
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def NiftiView(request):
	nifti_files = NiftiFiles.objects.all()
	nifti_dirs = NiftiDir.objects.all()
	context = {
		'all_files': nifti_files,
		'all_dirs': nifti_dirs
	}
	return render(request, 'nifti-view.html', context)

@login_required
def NiftiUpdate(request):
	settings.disable_validate_slice_increment()
	nifti_files = NiftiFiles.objects.all()
	nifti_dirs = NiftiDir.objects.all()
	context = {
		'all_files': nifti_files,
		'all_dirs': nifti_dirs
	}
	dicom_dir = MEDIA_ROOT / 'Dicom/'
	nifti_dirs = MEDIA_ROOT / 'Nifti/'
	dicom_dirs = [
		os.path.join(dicom_dir, x)
		for x in os.listdir(dicom_dir)
	]
	if not os.path.exists(nifti_dirs):
		os.makedirs(nifti_dirs)
	for study in dicom_dirs:
		nifti_dir = NiftiDir()
		nifti_dir.study_name = study.split("\\")[-1]
		nifti_dir.save()
		if not os.path.exists(nifti_dirs):
			os.makedirs(nifti_dir)
		dicom2nifti.dicom_series_to_nifti(dicom_dir, os.path.join(nifti_dirs, study.split("\\")[-1]), reorient_nifti=True)
	return redirect('/')
