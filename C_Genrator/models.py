from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib

class Certificate(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    recipient_name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    completion_date = models.DateField(default=timezone.now)
    unique_id = models.CharField(max_length=64, unique=True, blank=True, null=True)  # Unique ID field

    def save(self, *args, **kwargs):
        # Generate a unique ID based on certificate data
        certificate_data = f"{self.recipient_name}{self.course_name}{self.completion_date}"
        unique_id = hashlib.sha256(certificate_data.encode()).hexdigest()
        self.unique_id = unique_id
        super().save(*args, **kwargs)