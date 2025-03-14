from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Task, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_blocked')
    actions = ['block_users', 'unblock_users']

    def is_blocked(self, obj):
        try:
            return obj.userprofile.is_blocked
        except UserProfile.DoesNotExist:
            return False
    is_blocked.boolean = True
    is_blocked.short_description = 'Blocked'

    def block_users(self, request, queryset):
        for user in queryset:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_blocked = True
            profile.save()
    block_users.short_description = "Block selected users"

    def unblock_users(self, request, queryset):
        for user in queryset:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.is_blocked = False
            profile.save()
    unblock_users.short_description = "Unblock selected users"

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task)