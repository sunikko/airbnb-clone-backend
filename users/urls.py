from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("myprofile", views.Myprofile.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    path("@<str:username>/reviews", views.UserReviews.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
]