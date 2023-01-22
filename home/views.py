from django.shortcuts import render, redirect
from django.views import View
from .models import Meeting
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, "home/index.html")


class MeetingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_meeting = Meeting.objects.all().order_by("-timestamp")

        context = {
            "all_meeting": all_meeting
        }
        return render(request, "home/meeting.html", context)

    def post(self, request, *args, **kwargs):
        if Meeting.objects.filter(user=request.user).exists():
            pass
        else:
            meet = Meeting.objects.create(user=request.user, meeting_title="Title 1")
            return redirect("home:inside_meeting_view", SLUG=meet.slug)


class InsideMeetingView(LoginRequiredMixin, View):
    def get(self, request, SLUG, *args, **kwargs):
        try:
            current_meeting = Meeting.objects.get(slug=SLUG)
        except:
            return HttpResponse("<h3>Meeting no longer exist</h3>")


        context = {
            "current_meeting": current_meeting,
            #"img":img
        }
        return render(request, "home/inside-meeting.html", context)