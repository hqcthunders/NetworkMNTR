from django.urls import path, include
from . import views

app_name = 'networkmonitering'

urlpatterns = [
	path('', views.index, name='index'),
	path('interfaces/<slug:pk>', views.view_interfaces, name='view_interfaces')
]