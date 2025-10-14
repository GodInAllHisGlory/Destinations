from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("user/new", views.create_account, name="create_account"),
   path("user/", views.user, name="user"),
   path("session/new", views.sign_in, name="sign_in"),
   path("sessions", views.sessions, name="sessions"),
   path("destinations", views.destinations, name="destinations"),
   path("destinations/new", views.new_destination, name="new_destination"),
]