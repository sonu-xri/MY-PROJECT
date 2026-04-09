from django.db import models
from django.contrib.auth.models import User
import random
from django.db.models.signals import post_save
from django.dispatch import receiver


# ✅ OTP MODEL
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        """Generate 6 digit OTP"""
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def __str__(self):
        return f"{self.user.username} - {self.otp}"
    
    
    
#  ✅ login MODEL
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    role = models.CharField(max_length=10)
    
    last_login_time = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)


# Auto create profile when user created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

from django.db import models
from django.contrib.auth.models import User




class Resource(models.Model):
    
    def upload_path(self, filename):
        if self.teacher_student == "student":
            return f'student/{filename}'
        else:
            return f'teacher/{filename}'

    file = models.FileField(upload_to=upload_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    teacher_student = models.CharField(max_length=10)
    exam_year = models.CharField(max_length=10, null=True, blank=True)
    semester = models.CharField(max_length=10, null=True, blank=True)  
    exam_type = models.CharField(max_length=50, null=True, blank=True)




    def __str__(self):
        return self.title


# contact model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name