from django.urls import path
from . import views

urlpatterns = [
	path('', views.dicom, name='dicom_upload'),
	path('view/', views.dicom_view, name='dicom_view'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout')
]
