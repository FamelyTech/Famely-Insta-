import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class SnapshotInstagramUser(models.Model):
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    time = models.DateTimeField()


class InstagramUser(models.Model):
    user_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    profile_pic_url = models.CharField(max_length=1000, null=True)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    average_likes = models.FloatField()
    average_comments = models.FloatField()
    is_business = models.BooleanField(default=False)
    updated = models.DateTimeField("date updated")
    follow_snapshots = models.ManyToManyField(SnapshotInstagramUser, blank=True)

    def __str__(self):
        return f"{self.user_name}: {self.full_name}"

    def need_to_update(self):
        return self.updated < timezone.now() - datetime.timedelta(days=1)


class Theme(models.Model):
    name = models.CharField(max_length=200, unique=True)
    primary_background = models.CharField(max_length=200, blank=True, null=True)
    secondary_background = models.CharField(max_length=200, blank=True, null=True)
    text_color = models.CharField(max_length=200, blank=True, null=True)
    secondary_text_color = models.CharField(max_length=200, blank=True, null=True)
    navbar_background = models.CharField(max_length=200, blank=True, null=True)


class JalodeiUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, blank=True, null=True)
    instagram_username = models.CharField(max_length=200)
    instagram_password = models.CharField(max_length=200, blank=True, null=True)
    instagram_proxy = models.CharField(max_length=200)
    saved_users = models.ManyToManyField(InstagramUser, blank=True)

    def __str__(self):
        return f"ig username: {self.instagram_username}"


class InstagramComment(models.Model):
    user = models.ForeignKey(InstagramUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    content_type = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    like_count = models.IntegerField(default=0, blank=True, null=True)
    updated = models.DateTimeField("date updated")

    def __str__(self):
        return f"{self.text}"


class InstagramMediaScore(models.Model):
    category = models.CharField(max_length=2000, blank=True, null=True)
    score = models.FloatField()
    updated = models.DateTimeField("date updated")


class InstagramMedia(models.Model):
    user = models.ForeignKey(InstagramUser, on_delete=models.CASCADE, default=0)
    media_id = models.CharField(primary_key=True, max_length=200)
    media_type = models.IntegerField(default=0)
    caption_text = models.TextField(blank=True, null=True)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    play_count = models.IntegerField(blank=True, null=True)
    thumbnail_url = models.URLField(max_length=1000, blank=True, null=True)
    thumbnail_encoded = models.TextField(blank=True, null=True)
    video_url = models.URLField(max_length=1000, blank=True, null=True)
    media_datetime = models.DateTimeField()
    openai_comments_description = models.TextField(blank=True, null=True)
    hume_image_description = models.TextField(blank=True, null=True)
    updated = models.DateTimeField("date updated")
    media_likers = models.ManyToManyField(InstagramUser, related_name="likers", blank=True)
    media_comments = models.ManyToManyField(InstagramComment, blank=True)
    media_scores = models.ManyToManyField(InstagramMediaScore, blank=True)
    metadata = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.media_id}"

    def need_to_update(self):
        return self.updated < timezone.now() - datetime.timedelta(days=1)


class HumeFacialAnalysis(models.Model):
    media = models.ForeignKey(InstagramMedia, on_delete=models.CASCADE, default=0)
    media_pk = models.BigIntegerField(blank=True, null=True)
    admiration = models.DecimalField(max_digits=10, decimal_places=10)
    adoration = models.DecimalField(max_digits=10, decimal_places=10)
    aesthetic_appreciation = models.DecimalField(max_digits=10, decimal_places=10)
    amusement = models.DecimalField(max_digits=10, decimal_places=10)
    anger = models.DecimalField(max_digits=10, decimal_places=10)
    anxiety = models.DecimalField(max_digits=10, decimal_places=10)
    awe = models.DecimalField(max_digits=10, decimal_places=10)
    awkwardness = models.DecimalField(max_digits=10, decimal_places=10)
    boredom = models.DecimalField(max_digits=10, decimal_places=10)
    calmness = models.DecimalField(max_digits=10, decimal_places=10)
    concentration = models.DecimalField(max_digits=10, decimal_places=10)
    confusion = models.DecimalField(max_digits=10, decimal_places=10)
    contemplation = models.DecimalField(max_digits=10, decimal_places=10)
    contempt = models.DecimalField(max_digits=10, decimal_places=10)
    contentment = models.DecimalField(max_digits=10, decimal_places=10)
    craving = models.DecimalField(max_digits=10, decimal_places=10)
    desire = models.DecimalField(max_digits=10, decimal_places=10)
    determination = models.DecimalField(max_digits=10, decimal_places=10)
    disappointment = models.DecimalField(max_digits=10, decimal_places=10)
    disgust = models.DecimalField(max_digits=10, decimal_places=10)
    distress = models.DecimalField(max_digits=10, decimal_places=10)
    doubt = models.DecimalField(max_digits=10, decimal_places=10)
    ecstasy = models.DecimalField(max_digits=10, decimal_places=10)
    embarrassment = models.DecimalField(max_digits=10, decimal_places=10)
    empathic_pain = models.DecimalField(max_digits=10, decimal_places=10)
    entrancement = models.DecimalField(max_digits=10, decimal_places=10)
    envy = models.DecimalField(max_digits=10, decimal_places=10)
    excitement = models.DecimalField(max_digits=10, decimal_places=10)
    fear = models.DecimalField(max_digits=10, decimal_places=10)
    guilt = models.DecimalField(max_digits=10, decimal_places=10)
    horror = models.DecimalField(max_digits=10, decimal_places=10)
    interest = models.DecimalField(max_digits=10, decimal_places=10)
    joy = models.DecimalField(max_digits=10, decimal_places=10)
    love = models.DecimalField(max_digits=10, decimal_places=10)
    nostalgia = models.DecimalField(max_digits=10, decimal_places=10)
    pain = models.DecimalField(max_digits=10, decimal_places=10)
    pride = models.DecimalField(max_digits=10, decimal_places=10)
    realization = models.DecimalField(max_digits=10, decimal_places=10)
    relief = models.DecimalField(max_digits=10, decimal_places=10)
    romance = models.DecimalField(max_digits=10, decimal_places=10)
    sadness = models.DecimalField(max_digits=10, decimal_places=10)
    satisfaction = models.DecimalField(max_digits=10, decimal_places=10)
    shame = models.DecimalField(max_digits=10, decimal_places=10)
    surprise_negative = models.DecimalField(max_digits=10, decimal_places=10)
    surprise_positive = models.DecimalField(max_digits=10, decimal_places=10)
    sympathy = models.DecimalField(max_digits=10, decimal_places=10)
    tiredness = models.DecimalField(max_digits=10, decimal_places=10)
    triumph = models.DecimalField(max_digits=10, decimal_places=10)


class InstagramStoryMedia(models.Model):
    x = models.DecimalField(max_digits=10, decimal_places=8)
    y = models.DecimalField(max_digits=10, decimal_places=8)
    z = models.DecimalField(max_digits=10, decimal_places=8)
    width = models.DecimalField(max_digits=10, decimal_places=8)
    height = models.DecimalField(max_digits=10, decimal_places=8)
    rotation = models.DecimalField(max_digits=10, decimal_places=8)
    media_pk = models.CharField(max_length=200)


class InstagramStory(models.Model):
    user = models.ForeignKey(InstagramUser, on_delete=models.CASCADE)
    code = models.TextField(blank=True, null=True)
    story_datetime = models.DateTimeField()
    media_type = models.IntegerField(default=0)
    product_type = models.TextField(blank=True, null=True)
    thumbnail_url = models.URLField(max_length=1000, blank=True, null=True)
    thumbnail_encoded = models.TextField(blank=True, null=True)
    video_url = models.TextField(blank=True, null=True)
    video_duration = models.DecimalField(max_digits=10, decimal_places=3)
    sponsor_tags = models.ManyToManyField(InstagramUser, related_name="sponsors", blank=True)
    media = models.ManyToManyField(InstagramStoryMedia, blank=True)
