from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Meeting(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    meeting_title = models.CharField(max_length=255)
    qr_image = models.ImageField(blank=True, null=True, upload_to='QRCode')
    meeting_id = models.CharField(max_length=255)
    attendee = models.ManyToManyField(User, related_name="attendee")
    slug = models.SlugField()
    active = models.BooleanField(default=True)
    timestamp = models.DateField(auto_now_add=True)