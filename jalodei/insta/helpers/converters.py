from django.utils import timezone
from instagrapi.types import (Media as Instagrapi_Media, User as Instagrapi_User,
                              Story as Instagrapi_Story, StoryMedia as Instagrapi_StoryMedia,
                              UserShort, Comment)
from ..models import (InstagramMedia, InstagramUser, InstagramComment,
                      HumeFacialAnalysis, InstagramStory, InstagramStoryMedia)


def convert_shortuser(instagrapi_user_short: UserShort, check_full_users: bool = False) -> InstagramUser:
    if check_full_users:
        u = InstagramUser.objects.filter(user_name=instagrapi_user_short.username)
        if len(u) > 0:
            return u[0]
    return InstagramUser(
        pk=instagrapi_user_short.pk,
        user_name=instagrapi_user_short.username,
        full_name=instagrapi_user_short.full_name,
        profile_pic_url=instagrapi_user_short.profile_pic_url,
        average_likes=0.0,
        average_comments=0.0,
        updated=timezone.now()
    )

def convert_comment(instagrapi_comment: Comment) -> InstagramComment:
    return InstagramComment(
        user=convert_shortuser(instagrapi_comment.user),
        text=instagrapi_comment.text,
        created_timestamp=instagrapi_comment.created_at_utc,
        content_type=instagrapi_comment.content_type,
        status=instagrapi_comment.status,
        like_count=instagrapi_comment.like_count,
        updated=timezone.now()
    )


def convert_media(instagrapi_media: Instagrapi_Media, u) -> InstagramMedia:
    return InstagramMedia(
        user=u,
        media_id=instagrapi_media.pk,
        media_type=instagrapi_media.media_type,
        caption_text=instagrapi_media.caption_text,
        comment_count=instagrapi_media.comment_count,
        like_count=instagrapi_media.like_count,
        play_count=instagrapi_media.play_count,
        thumbnail_url=instagrapi_media.thumbnail_url,
        video_url=instagrapi_media.video_url,
        media_datetime=instagrapi_media.taken_at,
        updated=timezone.now()
    )


def convert_user(instagrapi_user: Instagrapi_User) -> InstagramUser:
    return InstagramUser(
        pk=instagrapi_user.pk,
        user_name=instagrapi_user.username,
        full_name=instagrapi_user.full_name,
        follower_count=instagrapi_user.follower_count,
        following_count=instagrapi_user.following_count,
        profile_pic_url=instagrapi_user.profile_pic_url,
        average_likes=0.0,
        average_comments=0.0,
        updated=timezone.now()
    )


def convert_facial_analysis(analysis, emotions) -> HumeFacialAnalysis:
    for emotion in emotions:
        attribute = emotion['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')
        score = emotion['score']
        setattr(analysis, attribute, score)

    return analysis


def convert_story(instagrapi_story: Instagrapi_Story, u) -> InstagramStory:
    return InstagramStory(
        user=u,
        code=instagrapi_story.code,
        story_datetime=instagrapi_story.taken_at,
        media_type=instagrapi_story.media_type,
        product_type=instagrapi_story.product_type,
        thumbnail_url=instagrapi_story.thumbnail_url,
        video_url=instagrapi_story.video_url,
        video_duration=instagrapi_story.video_duration
    )


def convert_story_media(instagrapi_story_media: Instagrapi_StoryMedia) -> InstagramStoryMedia:
    return InstagramStoryMedia(
        x=instagrapi_story_media.x,
        y=instagrapi_story_media.y,
        z=instagrapi_story_media.z,
        width=instagrapi_story_media.width,
        height=instagrapi_story_media.height,
        rotation=instagrapi_story_media.rotation,
        media_pk=instagrapi_story_media.media_pk
    )
