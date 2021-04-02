from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
PHONE_REGEX = RegexValidator(r'^01[0-2][0-9]{8}$', 'Egyptian phone number is required')
PASSWORD_REGEX = RegexValidator(r'.{6,}', 'Password must be at least 6 characters')

class User (models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20, validators=[PASSWORD_REGEX])
    phone = models.CharField(max_length=15, validators=[PHONE_REGEX])
    avatar = models.ImageField(upload_to="images/")
    is_admin = models.BooleanField(default=False)
    country = models.CharField(max_length=20, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    fb_account = models.URLField(blank=True, null=True)


    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)
