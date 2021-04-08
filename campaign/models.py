from datetime import timedelta
import datetime
from comment.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
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
    return User.objects.get_or_create(first_name='Anonymous', last_name='user')[0]


class Category(models.Model):
    label = models.CharField(max_length=50, unique=True)

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
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name="campaigns")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = TaggableManager(blank=True)
    comments = GenericRelation(Comment)

    def __str__(self):
        return str(self.title)

    errors = {}

    def clean(self):
        if (self.is_featured == True and Campaign.objects.filter(is_featured=True).exclude(id=self.id).count() >= 5):
            raise ValidationError(
                {'is_featured': _('You already have five featured campaigns.')})

        valid = True
        start_date = self.start_date
        end_date = self.end_date
        self.errors = {}
        if str(start_date) < str(datetime.date.today()):
            self.errors['date'] = 'invalid date'
            valid = False
        elif str(end_date) == str(start_date):
            self.errors['date'] = 'invalid date'
            valid = False
        elif str(end_date) < str(start_date):
            self.errors['date'] = 'invalid date'
            # 'End date should be greater than start date.'
            valid = False
        elif str(end_date) == str(datetime.date.today()):
            self.errors['date'] = 'invalid date'
            valid = False
        if self.title == '':
            self.errors['title'] = 'title is required'
            valid = False
        if self.details == '':
            self.errors['details'] = 'details is required'
            valid = False
        if self.target == '':
            self.errors['target'] = 'target is required'
            valid = False
        return valid


class CampaignReport(models.Model):
    details = models.TextField(max_length=2000)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.details)


class Rating(models.Model):
    value = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.value)

    class Meta:
        unique_together = ('campaign', 'user',)


class CampaignImage(models.Model):
    path = models.ImageField(upload_to='campaign', verbose_name='Image')

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return str(self.path)


class Donation(models.Model):
    amount = models.PositiveIntegerField()

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="donations")
    donator = models.ForeignKey(User, on_delete=models.SET(
        get_anonymous_user), default=None, related_name="donations")

    def __str__(self):
        return str(self.amount)
