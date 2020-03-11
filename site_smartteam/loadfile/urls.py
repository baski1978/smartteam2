
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home' ),
    path('empdetails', views.empdetails, name='empdetails'),
	path('projectteams/<indIdno>/',views.projectteams, name='projectteams' ),
    
]