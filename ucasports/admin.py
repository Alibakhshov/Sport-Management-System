from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
    "name",
    "email",
    "username",
    "is_staff",
    "is_active",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name", "bio", "avatar")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name", "bio", "avatar",)}),)
    

admin.site.register(CustomUser, UserAdmin)