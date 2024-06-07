from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=9, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="images", default=None, null=True, blank=True)
    birthday = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return f"User is {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

@property
def user_profile(self):
    return Profile.objects.get_or_create(user=self)[0]

User.profile = user_profile
