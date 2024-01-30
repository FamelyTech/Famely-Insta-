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
    instagram_save = models.BooleanField(default=False)
    instagram_proxy = models.CharField(max_length=200)
    saved_users = models.ManyToManyField(InstagramUser, blank=True)

    def __str__(self):
        return f"ig username: {self.instagram_username}"


class InstagramComment(models.Model):
    user = models.ForeignKey(InstagramUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000, blank=True, null=True)
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
    video_url = models.URLField(max_length=1000, blank=True, null=True)
    media_datetime = models.DateTimeField()
    aws_image_description = models.TextField(blank=True, null=True)
    openai_comments_description = models.TextField(blank=True, null=True)
    google_vision_image_description = models.TextField(blank=True, null=True)
    image_description = models.TextField(blank=True, null=True)
    updated = models.DateTimeField("date updated")
    media_likers = models.ManyToManyField(InstagramUser, related_name="likers", blank=True, null=True)
    media_comments = models.ManyToManyField(InstagramComment, blank=True, null=True)
    media_scores = models.ManyToManyField(InstagramMediaScore, blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.media_id}"

    def need_to_update(self):
        return self.updated < timezone.now() - datetime.timedelta(days=1)


class FacialAnalysis(models.Model):
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


class InstagramInsights(models.Model):
    user = models.ForeignKey(InstagramUser, on_delete=models.CASCADE, default=0)
    aiu_account_actions_graph_total_count = models.CharField(max_length=2000, blank=True, null=True)
    aiu_profile_visits_metric_count = models.IntegerField(blank=True, null=True)
    aiu_profile_visits_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_website_visits_metric_count = models.IntegerField(blank=True, null=True)
    aiu_website_visits_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_email_metric_count = models.IntegerField(blank=True, null=True)
    aiu_email_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_get_direction_metric_count = models.IntegerField(blank=True, null=True)
    aiu_get_direction_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_call_metric_count = models.IntegerField(blank=True, null=True)
    aiu_call_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_text_metric_count = models.IntegerField(blank=True, null=True)
    aiu_text_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_impressions_metric_count = models.IntegerField(blank=True, null=True)
    aiu_impressions_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_reach_metric_count = models.IntegerField(blank=True, null=True)
    aiu_reach_metric_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_hashtags_reach = models.CharField(max_length=2000, blank=True, null=True)
    aiu_last_week_impressions = models.IntegerField(blank=True, null=True)
    aiu_hashtags_impressions = models.CharField(max_length=2000, blank=True, null=True)
    aiu_product_page_view_count = models.CharField(max_length=2000, blank=True, null=True)
    aiu_product_page_view_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_product_save_count = models.CharField(max_length=2000, blank=True, null=True)
    aiu_product_save_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_product_direct_reshare_count = models.CharField(max_length=2000, blank=True, null=True)
    aiu_product_direct_reshare_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_product_button_click_count = models.IntegerField(blank=True, null=True)
    aiu_product_button_click_delta = models.CharField(max_length=2000, blank=True, null=True)
    aiu_account_discovery_graph_nodes = models.CharField(max_length=2000, blank=True, null=True)
    aiu_account_shopping_actions_graph_total_count_graph = models.CharField(max_length=2000, blank=True, null=True)
    aiu_graph_nodes = models.CharField(max_length=2000, blank=True, null=True)
    aiu_metric_graph_nodes = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_followers_unit_state = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_followers_delta_from_last_week = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_gender_graph = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_all_followers_age_graph = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_men_followers_age_graph = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_women_followers_age_graph = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_followers_top_cities_graph = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_followers_top_countries_graph = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_week_daily_followers_graph = models.CharField(max_length=2000, blank=True, null=True)
    followers_unit_days_hourly_followers_graphs = models.CharField(max_length=2000, blank=True, null=True)
