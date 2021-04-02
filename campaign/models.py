from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from user.models import User


def in_fourteen_days():
    return timezone.now() + timedelta(days=14)

def get_anonymous_user():
    return User.objects.get_or_create(first_name='Anonymous',last_name='user')[0]

class Campaign(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(max_length=2000)
    category = models.ForeignKey("Category",on_delete=models.PROTECT)
    target = models.PositiveIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=in_fourteen_days)
    creation_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    creator  = models.ForeignKey("user.User", on_delete=models.CASCADE,default=None)
    tags = TaggableManager()
    def __str__(self):
        return str(self.title)


class Category(models.Model):
    label = models.CharField(max_length=50)
    def __str__(self):
        return str(self.label)
    class Meta:
        verbose_name_plural = "Categories"

class CampaignReport(models.Model):
    details = models.TextField(max_length=2000)
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)
    reporter = models.ForeignKey("user.User", on_delete=models.CASCADE,default=None)
    def __str__(self):
        return str(self.details)


class Rating(models.Model):
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE,default=None)
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return str(self.value)


class CampaignImage(models.Model):
    path = models.ImageField(upload_to='static/images/', verbose_name='Image')
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)
    def __str__(self):
        return str(self.path)


class Comment(models.Model):
    content = models.TextField(max_length=1000, verbose_name='Comment')
    creation_date = models.DateTimeField(default=timezone.now)
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)
    creator = models.ForeignKey("user.User", on_delete=models.CASCADE,default=None)
    def __str__(self):
        return str(self.content)

class CommentReport(models.Model):
    details = models.TextField(max_length=2000, verbose_name='Report details')
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)
    reporter = models.ForeignKey("user.User", on_delete=models.CASCADE,default=None)
    def __str__(self):
        return str(self.details)

class Donation(models.Model):
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)
    donator = models.ForeignKey("user.User",on_delete=models.SET(get_anonymous_user),default=None)
    amount = models.PositiveIntegerField()
    def __str__(self):
        return str(self.amount)
