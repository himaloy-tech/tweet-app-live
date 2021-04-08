from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    liked_post = models.ManyToManyField('Post', blank=True, related_name="liked_posts")

class Post(models.Model):
    body = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_num = models.IntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name="like_users", blank=True)
    def likes_as_flat_user_id_list(self):
        return self.like_users.values_list('id', flat=True)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
    user_following = models.ManyToManyField(User, related_name="followers", blank=True)

    def __str__(self):
        return f"{self.user.username}"

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user_following = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return f"{self.user.username}"