from django.shortcuts import render, redirect
from django.views import View
from .models import Meeting
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import qrcode
import qrcode.image.svg
import time
from django.utils.text import slugify
from .otp_generator import meetingID

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
            meeting_title = request.POST.get("meeting_title")
            meeting_slug = slugify(meeting_title)
            meeting_id = meetingID()

            #QR code
            # Data to encode
            data = f"https://domain/meeting-verification/complete/{meeting_slug}/{meeting_id}/"
            # Creating an instance of QRCode class
            qr = qrcode.QRCode(version = 1,
                box_size = 10,
                border = 5)
            #Adding data to the instance 'qr'
            qr.add_data(data)
            
            qr.make(fit = True)
            img = qr.make_image(fill_color = 'red',
                                back_color = 'white')
            img_name = f'/QRCode/{meeting_slug}'+str(time.time())+'.png'
            img.save(settings.MEDIA_ROOT + img_name)

            meet = Meeting.objects.create(
                user=request.user, meeting_title=meeting_title, qr_image=img_name, slug=meeting_slug, meeting_id=meeting_id
            )
            return redirect("home:inside_meeting_view", SLUG=meet.slug, MEETING_ID=meeting_id)


class MeetingVerification(LoginRequiredMixin, View):
    def get(self, request, SLUG, *args, **kwargs):
        try:
            current_meeting = Meeting.objects.get(slug=SLUG)
        except:
            return HttpResponse("<h3>Meeting no longer exist</h3>")
        attendee = request.user
        verification = False
        for i in current_meeting.attendee.all():
            if i == attendee:
                verification = True
                break
        if verification:
            return redirect("home:inside_meeting_view", SLUG=current_meeting.slug)
        else:
            return HttpResponse("<h3>Scan the QR Code on the meeting ground to gain access</h3>")


class MeetingVerificationComplete(LoginRequiredMixin, View):
    def get(self, request, SLUG, MEETING_ID, *args, **kwargs):
        try:
            current_meeting = Meeting.objects.get(slug=SLUG, meeting_id=MEETING_ID)
        except:
            return HttpResponse("<h3>Meeting no longer exist</h3>")
        current_meeting.attendee.add(request.user)
        return redirect("home:inside_meeting_view", SLUG=current_meeting.slug)


class InsideMeetingView(LoginRequiredMixin, View):
    def get(self, request, SLUG, MEETING_ID, *args, **kwargs):
        try:
            current_meeting = Meeting.objects.get(slug=SLUG, meeting_id=MEETING_ID)
            print(current_meeting.qr_image.url)
        except:
            return HttpResponse("<h3>Meeting no longer exist</h3>")


        context = {
            "current_meeting": current_meeting,
        }
        return render(request, "home/inside-meeting.html", context)