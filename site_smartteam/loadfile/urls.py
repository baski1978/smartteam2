
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home' ),
	path('projectteams',views.projectteams, name='projectteams' )
]
