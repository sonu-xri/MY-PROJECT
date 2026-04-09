from django.contrib import admin
from .models import Resource, UserProfile
from .models import Contact


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_login_time', 'login_count')


admin.site.register(Resource)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Contact)
