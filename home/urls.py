from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home_view"),
    path('meeting/', views.MeetingView.as_view(), name="meeting_view"),
    path('meeting/<slug:SLUG>/', views.InsideMeetingView.as_view(), name="inside_meeting_view"),
]