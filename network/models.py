from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime
import pytz
from django.utils import timezone


class User(AbstractUser):
    image = models.CharField(max_length=500,default="https://i.pinimg.com/originals/0c/3b/3a/0c3b3adb1a7530892e55ef36d3be6cb8.png")
    followers = models.ManyToManyField("self", related_name="following", blank=True, symmetrical=False)
    def number_of_followers(self):
        return len(self.followers.all())
    def number_of_following(self):
        return len(self.following.all())


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    time = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    public = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)

    def liked(self):
        return self.likes.all().count()

    def __str__(self):
        return f'Post by {self.user} says, "{self.body}". Has {self.liked()} like{"s" if self.liked() != 1 else ""}.'

    def serialize(self, tzname=None, logged_user=None):
        if not tzname:
            tzname = "Asia/Kolkata"
        timezone.activate(pytz.timezone(tzname))
        return {
            "id": self.id,
            "user": self.user.username,
            "author":self.user.first_name + ' ' + self.user.last_name,
            "body": self.body,
            "time": localtime(self.time).strftime('%b %d, %I:%M %p'),
            "likedby": [user.id for user in self.likes.all()],
            "likes": self.likes.all().count()
        }


class Profile(models.Model):
    target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='folowers')
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='targets')
  
class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.post)
