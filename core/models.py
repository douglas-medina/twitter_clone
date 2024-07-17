from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.

class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    groups = models.ManyToManyField(
        Group,
        related_name='core_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='core_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content