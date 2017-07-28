from hashlib import sha256
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime as dt

# Create your models here.


def get_hash(email):
    h = sha256()
    h.update(email.encode('utf-8'))
    return h.hexdigest()[:50]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(auto_now=False, default=dt(1970, 1, 1))
    verification_code = models.CharField(null=False, blank=True, max_length=50)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.verification_code = get_hash(self.user.email)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

