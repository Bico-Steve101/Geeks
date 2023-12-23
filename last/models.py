import math
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    # name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    tag = models.CharField(max_length=100, null=True)
    project_description = models.TextField(null=True)
    joined = models.DateTimeField(auto_now_add=True)
    # login = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(null=True, upload_to="media\profile",
                               default="media/geeks_projects/steve-rebrand-logo.png")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Hackathons(models.Model):
    founder = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="hackathon_founder", null=True, )
    name = models.CharField(max_length=200)
    theme = models.TextField(null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    prize = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='media\geeks_projects', default='media/geeks_projects/steve-rebrand-logo.png')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Grade(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hackathon = models.ForeignKey(Hackathons, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.participant.username} in {self.hackathon.name}"


class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    link = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='media\geeks_projects', default='media/geeks_projects/steve-rebrand-logo.png')

    def __str__(self):
        return self.title

    def time_created(self):
        now = timezone.now()

        diff = now - self.created_at

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if 1 <= diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def serialize(self):
        return {"time": self.created_at, "title": self.title, "description": self.description, "link": self.link}


class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=500)
    link = models.TextField(max_length=100)
    image = models.ImageField(upload_to='media\geeks_projects', default='media/user_profile/steve-rebrand-logo.png')

    def __str__(self):
        return self.user.username


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=500)
    link = models.TextField(max_length=100)
    image = models.ImageField(default='media/user_profile/steve-rebrand-logo.png')


def __str__(self):
    return self.user.username


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(upload_to='media/user_profile', default='media/user_profile/steve-rebrand-logo.png')
    user_tag = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=254, blank=True, unique=True)
    user_name = models.CharField(max_length=100)
    login = models.DateTimeField(null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=200)
    describe = models.TextField(max_length=200)

    def __str__(self):
        return self.user.username
