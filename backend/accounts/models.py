from django.db import models
from django.contrib.auth.models import User

class Following(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers_set', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
