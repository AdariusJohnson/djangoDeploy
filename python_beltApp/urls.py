from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('travels', views.success),
    path('logout', views.logout),
    path('login', views.login),
    path('addtrip', views.addTrip),
    path('uploadTrip', views.uploadTrip),
    path('view/<int:tripId>', views.tripInfo),
    path('joinTrip/<int:tripId>', views.joinTrip),
    path('removeTrip/<int:tripId>', views.removeTrip),
    path('deleteTrip/<int:tripId>', views.deleteTrip),
]