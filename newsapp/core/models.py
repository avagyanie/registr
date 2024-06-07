from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from django.contrib.auth.models import User
import datetime
from django.utils import timezone



# Create your models here.
User = get_user_model()

class News(models.Model):

    NEWS_TYPES = (
        ("1", "Political"),
        ("2", "Business"),
        ("3", "International"),
        ("4","National"),
        ("5","Lifestyle"),
        ("6", "Sport"),
        ("7", "Cultural"),
        ("8", "Crime")
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    news_type = models.CharField(choices=NEWS_TYPES, default="4", max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default=None, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title}, {self.news_type}, {self.user},{self.date}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 700:
            output_size = (500, 700)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Team(models.Model):
    team_member=models.CharField(max_length=30)
    position=models.CharField(max_length=30)
    description=models.TextField(max_length=300)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"{self.team_member}" 

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})


class Message(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank = True, null = True)

    def __str__(self) -> str:
        return f"{self.full_name}, {self.date}"


class NewsComment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"{self.owner.username} is commented {self.text}"


class TeamMember(models.Model):
    full_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="Media", default=None, null=True, blank=True)
    linkedin=models.CharField(max_length=100,default=None, null=True, blank=True)



class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.email


class Info(models.Model):
    app_name = models.CharField(max_length=9)
    about = models.TextField(max_length=1000)
    mission = models.TextField(max_length=1000)
    latest_news_text1 = models.TextField(max_length=1000)
    latest_news_text2 = models.TextField(max_length=1000)
    about_team = models.TextField(max_length=1000)
    pub_date = models.DateTimeField(auto_now_add= True)

    def yearpublished(self):
        current_year = timezone.now().year
        return current_year
    
    def __str__(self) -> str:
        return f"App - {self.app_name}"


class Contact(models.Model):
    address = models.CharField(max_length=50)
    tel = models.CharField(max_length=13)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"Address - {self.address}, tel - {self.tel}, email - {self.email}"
