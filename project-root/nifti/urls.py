from django.urls import path
from . import views
from dicom.views import user_logout

urlpatterns = [
	path('', views.NiftiView, name='nifti-view'),
	path('logout/', user_logout, name='logout'),
	path('update/', views.NiftiUpdate, name='update'),
]
