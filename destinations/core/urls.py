from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("user/new", views.create_account, name="create_account"),
]