import os
from django.conf import settings
from django.utils import timezone
from itertools import repeat
from typing import List
from ..models import (InstagramMedia, InstagramUser, JalodeiUser, SnapshotInstagramUser)
from ..helpers.converters import (convert_media, convert_shortuser, convert_user)


def get_user_display(request, display_user: str) -> InstagramUser:
    u = InstagramUser.objects.filter(user_name=display_user)
    request_user = JalodeiUser.objects.get(user=request.user)

    new_display_user = False

    if len(u) != 1:
        new_display_user = True
    else:
        u = u[0]

    if new_display_user or u.need_to_update():
        try:
            cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)
            display_user_info = cl.user_info_by_username(display_user)
        except Exception as e:
            os.remove(f"{settings.BASE_DIR}/session.json")
            cl = inst_set_proxy(request_user.instagram_proxy)
            cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)
            display_user_info = cl.user_info_by_username(display_user)

        u = convert_user(display_user_info)
        u.save()

    if request_user.instagram_username != display_user:
        request_user.saved_users.add(u)

    snapshot = SnapshotInstagramUser(
            followers=u.follower_count,
            following=u.following_count,
            time=timezone.now()
        )

    snapshot.save()

    u.follow_snapshots.add(snapshot)

    return u


def get_top_hashtag_display(request, hashtag: str) -> List[InstagramMedia]:
    u = InstagramMedia.objects.filter(caption_text__icontains=hashtag)

    request_user = JalodeiUser.objects.get(user=request.user)
    cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)

    hashtag_media = cl.hashtag_medias_top(hashtag, 10)

    media_list = []

    for m in hashtag_media:
        post_user = convert_shortuser(m.user)
        post_user.save()
        m = convert_media(m, post_user)
        media_list.append(m)
        m.save()

    return media_list


def get_recent_hashtag_display(request, hashtag: str) -> List[InstagramMedia]:
    request_user = JalodeiUser.objects.get(user=request.user)
    cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)

    hashtag_media = cl.hashtag_medias_recent(hashtag)

    media_list = []

    for m in hashtag_media:
        post_user = convert_shortuser(m.user)
        post_user.save()
        m = convert_media(m, post_user)
        media_list.append(m)
        m.save()

    return media_list


def get_related_hashtag_display(request, hashtag: str) -> List[Hashtag]:
    request_user = JalodeiUser.objects.get(user=request.user)
    cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)

    hashtags = cl.hashtag_related_hashtags("soccer")

    return hashtags


def get_usertag_display(request, display_user: str) -> List[InstagramMedia]:
    request_user = JalodeiUser.objects.get(user=request.user)
    cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)
    display_user_id = cl.user_info_by_username(display_user)
    display_user_id = display_user_id.pk
    usertag_media = cl.usertag_medias(display_user_id, 100)
    media_list = []

    for m in usertag_media:
        post_user = convert_shortuser(m.user)
        post_user.save()
        m = convert_media(m, post_user)
        media_list.append(m)
        m.save()

    return media_list


def get_media_display(request, display_user: str) -> List[InstagramMedia]:
    u = InstagramUser.objects.get(user_name=display_user)
    detailed_media_list = (InstagramMedia.objects.filter(user=u.pk)
                           .exclude(openai_comments_description__isnull=True))

    request_user = JalodeiUser.objects.get(user=request.user)
    cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)

    media_amount = 100
    media_api_list = cl.user_medias(u.pk, amount=media_amount)
    media_list = list(map(convert_media, media_api_list, repeat(u)))

    for m in media_list:
        detailed_media = next((x for x in detailed_media_list if x.media_id == m.media_id), None)

        m.save()

        if detailed_media is not None:
            media_list[media_list.index(m)] = detailed_media

    return media_list
