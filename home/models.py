from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import qrcode

# Create your models here.

class Meeting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meeting_title = models.CharField(max_length=255)
    qr_image = models.ImageField(blank=True, null=True, upload_to='QRCode')
    slug = models.SlugField()
    active = models.BooleanField(default=True)
    timestamp = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        #QR Code
        data = "GeeksforGeeks"
        qr_image = qrcode.make(self.meeting_title)

        #Slug
        self.slug = slugify(self.meeting_title)
        super(Meeting, self).save(*args, **kwargs)