from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('travels', views.travels),
    path('travels/destination/<trip_id>', views.show),
    path('travels/add', views.add),
    path('create', views.create),
    path('join/<trip_id>', views.join),
    path('gowith/<trip_id>', views.gowith),

]