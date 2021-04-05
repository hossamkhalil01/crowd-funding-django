from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from taggit.managers import TaggableManager
from user.models import User


def in_fourteen_days():
    return timezone.now() + timedelta(days=14)

def get_anonymous_user():
    return User.objects.get_or_create(first_name='Anonymous',last_name='user')[0]

class Category(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name_plural = "Categories"

class Campaign(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField(max_length=2000)
    target = models.PositiveIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=in_fourteen_days)
    creation_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="campaigns")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return str(self.title)

    def clean(self):
        if (self.is_featured == True and Campaign.objects.filter(is_featured=True).exclude(id=self.id).count() >= 5):
            raise ValidationError({'is_featured':_('You already have five featured campaigns.')})

class CampaignReport(models.Model):
    details = models.TextField(max_length=2000)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.details)


class Rating(models.Model):
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.value)
        
    class Meta:
        unique_together = ('campaign', 'user',)

class CampaignImage(models.Model):
    path = models.ImageField(upload_to='campaign', verbose_name='Image')

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return str(self.path)


class Comment(models.Model):
    content = models.TextField(max_length=1000, verbose_name='Comment')
    creation_date = models.DateTimeField(default=timezone.now)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="comments")
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='replies')
    def __str__(self):
        return str(self.content)


class CommentReport(models.Model):
    details = models.TextField(max_length=2000, verbose_name='Report details')

    comment = models.ForeignKey(Comment, default=None, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.details)


class Donation(models.Model):
    amount = models.PositiveIntegerField()

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="donations")
    donator = models.ForeignKey(User, on_delete=models.SET(get_anonymous_user),default=None, related_name="donations")

    def __str__(self):
        return str(self.amount)
