from django.urls import path
from . import views


urlpatterns = [
    path("", views.RoomListView.as_view()),
    path("<int:pk>", views.RoomDetailView.as_view()),
    path("<int:pk>/reviews", views.RoomReviews.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenityDetail.as_view()),
]