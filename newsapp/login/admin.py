from django.contrib import admin
from django.apps import AppConfig
from .models import Profile


# Register your models here.
class AccountsConfig(AppConfig):
    name = 'accounts'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('tel', )
    