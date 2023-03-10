from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home_view"),
    path('meeting/', views.MeetingView.as_view(), name="meeting_view"),
    path('meeting-verification/<slug:SLUG>/', views.MeetingVerification.as_view(), name="meeting_verification"),
    path('meeting-verification/complete/<slug:SLUG>/<str:MEETING_ID>/', views.MeetingVerification.as_view(), name="meeting_verification"),
    path('meeting/<slug:SLUG>/', views.InsideMeetingView.as_view(), name="inside_meeting_view"),
]