from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver

SEE = [
    ('unseen', 'unseen'),
    ('present', 'present'),
    ('seen', 'seen'),
]

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visits = models.IntegerField(default=0)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=9, choices=GENDER, blank=True, null=True)
    birthday = models.CharField(max_length=20, blank=True, null=True, )
    job = models.CharField(max_length=20, blank=True, null=True, )
    email_confirmed = models.BooleanField(default=False)
    dp = models.ImageField(upload_to='images/', blank=True, null=True, )
    country = models.CharField(max_length=20, blank=True, default='Nigeria')
    state = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=230, default="Hi welcome to my profile.")
    twitter = models.CharField(max_length=22, blank=True, null=True, default='', help_text="Don't add '@'")
    instagram = models.CharField(max_length=22, blank=True, null=True, default=' ')
    facebook = models.CharField(max_length=22, blank=True, null=True, default=' ')
    linkedin = models.CharField(max_length=22, blank=True, null=True, default=' ')
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    post_pic = models.ImageField(upload_to='post_pics/', null=True, blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='post_likes')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)
    not_status = models.CharField(max_length=10, choices=SEE, default='unseen')
    visits = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    not_status = models.CharField(max_length=10, choices=SEE, default='unseen')
    body = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dp = models.ImageField(upload_to="comment_dp", null=True)
    comment_pic = models.ImageField(upload_to='comment_pics/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    visits = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('comment_detail', args=[str(self.id)])


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    dp = models.ImageField(upload_to="comment_dp", null=True)
    comment_pic = models.ImageField(upload_to='comment_pics/', null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='reply_likes')
    created_on = models.DateTimeField(auto_now_add=True)
    not_status = models.CharField(max_length=10, choices=SEE, default='unseen')


class Notification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    not_status = models.CharField(max_length=10, choices=SEE, default='unseen')
    created_on = models.TimeField(auto_now_add=True)
