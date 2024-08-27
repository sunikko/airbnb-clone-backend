from django.urls import path
from . import views

urlpatterns = [
    path("myprofile", views.Myprofile.as_view()),
]