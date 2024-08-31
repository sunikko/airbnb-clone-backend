from django.urls import path
from . import views


urlpatterns = [
    path('', views.ExperienceListView.as_view()),
    path('perks/', views.PerkListView.as_view()),
    path('perks/<int:pk>', views.PerkDetail.as_view()),
]