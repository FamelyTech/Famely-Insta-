from django.utils import timezone
from ..models import (InstagramInsights, InstagramMedia, InstagramUser, InstagramComment,
                      FacialAnalysis)


def convert_shortuser(inst_user_short: UserShort) -> InstagramUser:
    return InstagramUser(
        pk=inst_user_short.pk,
        user_name=inst_user_short.username,
        full_name=inst_user_short.full_name,
        profile_pic_url=inst_user_short.profile_pic_url,
        average_likes=0.0,
        average_comments=0.0,
        updated=timezone.now()
    )

def convert_comment(inst_comment: Comment) -> InstagramComment:
    return InstagramComment(
        user=convert_shortuser(inst_comment.user),
        text=inst_comment.text,
        created_timestamp=inst_comment.created_at_utc,
        content_type=inst_comment.content_type,
        status=inst_comment.status,
        like_count=inst_comment.like_count,
        updated=timezone.now()
    )


def convert_insights(insights, u) -> InstagramInsights:
    return InstagramInsights(
        user=u,
        aiu_account_actions_graph_total_count=insights.aiu_account_actions_graph_total_count,
        aiu_profile_visits_metric_count=insights.aiu_profile_visits_metric_count,
        aiu_profile_visits_metric_delta=insights.aiu_profile_visits_metric_delta,
        aiu_website_visits_metric_count=insights.aiu_website_visits_metric_count,
        aiu_website_visits_metric_delta=insights.aiu_website_visits_metric_delta,
        aiu_email_metric_count=insights.aiu_email_metric_count,
        aiu_email_metric_delta=insights.aiu_email_metric_delta,
        aiu_get_direction_metric_count=insights.aiu_get_direction_metric_count,
        aiu_get_direction_metric_delta=insights.aiu_get_direction_metric_delta,
        aiu_call_metric_count=insights.aiu_call_metric_count,
        aiu_call_metric_delta=insights.aiu_call_metric_delta,
        aiu_text_metric_count=insights.aiu_text_metric_count,
        aiu_text_metric_delta=insights.aiu_text_metric_delta,
        aiu_impressions_metric_count=insights.aiu_impressions_metric_count,
        aiu_impressions_metric_delta=insights.aiu_impressions_metric_delta,
        aiu_reach_metric_count=insights.aiu_reach_metric_count,
        aiu_reach_metric_delta=insights.aiu_reach_metric_delta,
        aiu_hashtags_reach=insights.aiu_hashtags_reach,
        aiu_last_week_impressions=insights.aiu_last_week_impressions,
        aiu_hashtags_impressions=insights.aiu_hashtags_impressions,
        aiu_product_page_view_count=insights.aiu_product_page_view_count,
        aiu_product_page_view_delta=insights.aiu_product_page_view_delta,
        aiu_product_save_count=insights.aiu_product_save_count,
        aiu_product_save_delta=insights.aiu_product_save_delta,
        aiu_product_direct_reshare_count=insights.aiu_product_direct_reshare_count,
        aiu_product_direct_reshare_delta=insights.aiu_product_direct_reshare_delta,
        aiu_product_button_click_count=insights.aiu_product_button_click_count,
        aiu_product_button_click_delta=insights.aiu_product_button_click_delta,
        aiu_account_discovery_graph_nodes=insights.aiu_account_discovery_graph_nodes,
        aiu_account_shopping_actions_graph_total_count_graph=insights.aiu_account_shopping_actions_graph_total_count_graph,
        aiu_graph_nodes=insights.aiu_graph_nodes,
        aiu_metric_graph_nodes=insights.aiu_metric_graph_nodes,
        followers_unit_followers_unit_state=insights.followers_unit_followers_unit_state,
        followers_unit_followers_delta_from_last_week=insights.followers_unit_followers_delta_from_last_week,
        followers_unit_gender_graph=insights.followers_unit_gender_graph,
        followers_unit_all_followers_age_graph=insights.followers_unit_all_followers_age_graph,
        followers_unit_men_followers_age_graph=insights.followers_unit_men_followers_age_graph,
        followers_unit_women_followers_age_graph=insights.followers_unit_women_followers_age_graph,
        followers_unit_followers_top_cities_graph=insights.followers_unit_followers_top_cities_graph,
        followers_unit_followers_top_countries_graph=insights.followers_unit_followers_top_countries_graph,
        followers_unit_week_daily_followers_graph=insights.followers_unit_week_daily_followers_graph,
        followers_unit_days_hourly_followers_graphs=insights.followers_unit_days_hourly_followers_graphs
    )


def convert_media(inst_media: Inst_Media, u) -> InstagramMedia:
    return InstagramMedia(
        user=u,
        media_id=inst_media.pk,
        media_type=inst_media.media_type,
        caption_text=inst_media.caption_text,
        comment_count=inst_media.comment_count,
        like_count=inst_media.like_count,
        play_count=inst_media.play_count,
        thumbnail_url=inst_media.thumbnail_url,
        video_url=inst_media.video_url,
        media_datetime=inst_media.taken_at,
        updated=timezone.now()
    )


def convert_user(inst_user: Inst_User) -> InstagramUser:
    return InstagramUser(
        pk=inst_user.pk,
        user_name=inst_user.username,
        full_name=inst_user.full_name,
        follower_count=inst_user.follower_count,
        following_count=inst_user.following_count,
        profile_pic_url=inst_user.profile_pic_url,
        average_likes=0.0,
        average_comments=0.0,
        updated=timezone.now()
    )


def convert_facial_analysis(analysis, emotions) -> FacialAnalysis:
    for emotion in emotions:
        attribute = emotion['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')
        score = emotion['score']
        setattr(analysis, attribute, score)

    return analysis
