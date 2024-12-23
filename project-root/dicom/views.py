from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .models import DicomFiles, DicomDirs, DicomUpdates, DicomStudyTypes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
import sys
import json

SMARTCAPTCHA_SERVER_KEY = "ysc2_XXhT1bV9bGaaBRNj8nOaTOOXxY2kTRUls86pmvGgc6eeb0c6"

# Create your views here.

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

def check_captcha(token, request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
        	ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	resp = requests.post(
		"https://smartcaptcha.yandexcloud.net/validate",
		data={
			"secret": SMARTCAPTCHA_SERVER_KEY,
			"token": token,
			"ip": ip   # Способ получения IP-адреса зависит от вашего фреймворка и прокси.
                                            # Например, во Flask это может быть request.remote_addr
		},
		timeout=1
	)
	server_output = resp.content.decode()
	if resp.status_code != 200:
		print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
		return True
	return json.loads(server_output)["status"] == "ok"

def user_login(request):
	if request.POST:
		token = request.POST['smart-token']  # Например, request.form["smart-token"]
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			if check_captcha(token, request):
				print("Passed")
				login(request, user=user)
				return redirect('dicom_upload')
			else:
				print("Robot")
	return render(request, 'login.html')

def user_logout(request):
	logout(request)
	return redirect('login')
