from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class UserModel(models.Model):

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return "%s's profile" % self.user

    user = models.OneToOneField(User)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserModel.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Food(models.Model):

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Foods"

    def __str__(self):
        pass

    name = models.CharField(max_length=100)
    description = models.TextField()
    serving_size = models.IntegerField()
    deadline = models.DateTimeField()
    owner = models.ForeignKey(UserModel)
