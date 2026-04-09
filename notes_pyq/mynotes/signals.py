from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from .models import UserProfile

@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.last_login_time = now()
    profile.save()