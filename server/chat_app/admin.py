from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Chat, Message, Request

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'bio', 'avatar_url']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'avatar_public_id', 'avatar_url')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'avatar_public_id', 'avatar_url')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Request)
admin.site.register(Code)
