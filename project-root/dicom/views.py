import sys
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.models import Permission
from .models import DicomFiles, DicomDirs, DicomUpdates, DicomStudyTypes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def dicom_view(request):
    dicom_files = DicomFiles.objects.all()
    dicom_dirs = DicomDirs.objects.all()
    context = {
        'all_files': dicom_files,
        'all_dirs': dicom_dirs
    }
    return render(request, 'dicom-view.html', context)

@login_required
def dicom(request):
    if request.POST:
        dicom_dir = DicomDirs()
        dicom_dir.study_name = request.POST.get('folder')
        dicom_dir.screens = request.POST.get('screens').split(",")
        dicom_dir.study_type = DicomStudyTypes.objects.get(id=request.POST.get('select-type'))
        dicom_dir.save()
        update = DicomUpdates()
        update.user = request.user
        update.dir =  DicomDirs.objects.latest('id')
        update.save()
        for dir in request.FILES.getlist('file_field'):
            dicom = DicomFiles()
            dicom.study_id = DicomDirs.objects.latest('id')
            dicom.dir = dir
            dicom.save()
    return render(request, 'dicom-upload.html')

def user_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user=user)
            return redirect('dicom_upload')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')