from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from .forms import InstagramForm, JalodeiUserConfiguration
from .helpers.ai import analyze_face, hume_analyze_image, openai_analyze_comments, rate_image
from .helpers.converters import convert_comment, convert_facial_analysis, convert_shortuser
from .helpers.display import (get_media_display, get_usertag_display,
                              get_top_hashtag_display, get_user_display, get_stories_display)
from .helpers.instagrapi import instagrapi_error_context, instagrapi_login_client, instagrapi_set_proxy
from .models import HumeFacialAnalysis, InstagramMedia, InstagramUser, JalodeiUser, Theme
import base64
import httpx


def index(request):
    try:
        context = {}
        if request.method == 'POST':
            form = InstagramForm(request.POST)
            form_account = form.cleaned_data['account_name']
            form_media = form.cleaned_data['media_id']
            context = {'form': form}
            if form.is_valid():
                context.update({'form_media': form_media,
                                'form_account': form_account})

        if request.user.is_authenticated:
            jalodei_user = JalodeiUser.objects.filter(user=request.user)
        else:
            context = {'form': AuthenticationForm()}
            return render(request, 'registration/login.html', context)
        if len(jalodei_user) == 0:
            return redirect('create_jalodei_user')
        else:
            jalodei_user = jalodei_user[0]
        template = loader.get_template('insta/index.html')
        ig_user = InstagramUser.objects.filter(user_name=jalodei_user.instagram_username)
        if len(ig_user) < 1:
            ig_user = get_user_display(request, jalodei_user.instagram_username)
        else:
            ig_user = ig_user[0]

        context.update({'active_user': ig_user,
                        'theme': jalodei_user.theme,
                        'saved_ig_users': jalodei_user.saved_users.all()})

        return HttpResponse(template.render(context, request))

    except Exception as e:
        context = instagrapi_error_context(e)
        return render(request, 'insta/error_detail.html', context)


def create_jalodei_user(request):
    if request.method == 'POST':
        form = JalodeiUserConfiguration(request.POST)
        if form.is_valid():
            theme = Theme.objects.all()[0]
            jalodei_user = JalodeiUser(
                user=request.user,
                theme=theme,
                instagram_username=form.cleaned_data['instagram_user'],
                instagram_password=form.cleaned_data['instagram_password'],
                instagram_proxy=form.cleaned_data['proxy'],
            )
            jalodei_user.save()
            return redirect('index')
    else:
        form = JalodeiUserConfiguration()
    return render(request, 'insta/create_jalodei_user.html', {'form': form})


def account_detail(request, user_name):
    user_name = user_name.lower()
    template = loader.get_template('insta/account_detail.html')
    jalodei_user = JalodeiUser.objects.get(user=request.user)

    try:
        user_display_info = get_user_display(request, user_name)
    except Exception as e:
        context = instagrapi_error_context(e)
        return render(request, 'insta/error_detail.html', context)

    encoded_image = base64.b64encode(httpx.get(user_display_info.profile_pic_url).content).decode("utf-8")

    user_display_info.save()

    media_display_info = get_media_display(request, user_name)

    story_display_info = get_stories_display(request, user_display_info)

    top_hashtag_display_info = get_top_hashtag_display(request, user_name)

    usertag_display_info = get_usertag_display(request, user_name)

    context = {'user': user_display_info,
               'encoded_image': encoded_image,
               'theme': jalodei_user.theme,
               'media_list': media_display_info,
               'top_hashtag_list': top_hashtag_display_info,
               'story_list': story_display_info,
               'usertag_list': usertag_display_info}

    return HttpResponse(template.render(context, request))


def media_detail(request, media_pk):
    jalodei_user = JalodeiUser.objects.get(user=request.user)
    template = loader.get_template('insta/media_detail.html')
    media_likers, media_comments = get_media_details(request, media_pk)

    media = InstagramMedia.objects.get(media_id=media_pk)
    facial_analysis = []

    if media.thumbnail_url is not None:
        hume_response = hume_analyze_image(media.thumbnail_url)
        media.hume_image_description = hume_response
        facial_analysis = analyze_face(hume_response)

        if facial_analysis != '':
            analysis = HumeFacialAnalysis.objects.filter(media=media)
            if len(analysis) < 1:
                analysis = HumeFacialAnalysis()
                analysis.media = media
                analysis.media_pk = media.media_id
            else:
                analysis = analysis[0]

            analysis = convert_facial_analysis(analysis, facial_analysis)
            analysis.save()

            for emotion in facial_analysis:
                emotion['score'] = f"{str(emotion['score'])[2:4]}.{str(emotion['score'])[4:7]}%"

    else:
        media.hume_image_description = None

    openai_comments_analysis = openai_analyze_comments(media_comments)
    media.openai_comments_description = openai_comments_analysis

    if media.thumbnail_url:
        summary = rate_image(media, media_comments)
    else:
        summary = "no image to analyze"

    media.save()

    context = {'media_liker_list': media_likers,
               'media': media,
               'theme': jalodei_user.theme,
               'media_comment_list': media_comments,
               'media_pk': media_pk,
               'facial_analysis': facial_analysis,
               'openai_comments_analysis': openai_comments_analysis,
               'summary': summary}

    return HttpResponse(template.render(context, request))


def error_detail(request, context):
    template = loader.get_template('insta/error_detail.html')

    return HttpResponse(template.render(context, request))


def get_media_details(request, media_pk):
    request_user = JalodeiUser.objects.get(user=request.user)
    cl = instagrapi_set_proxy(request_user.instagram_proxy)
    cl = instagrapi_login_client(cl, request_user.instagram_username, request_user.instagram_password)
    media = InstagramMedia.objects.get(media_id=media_pk)

    media_likers = cl.media_likers(media_pk)
    media_liker_list = []

    for media_liker in media_likers:
        liker_user = convert_shortuser(media_liker, True)
        liker_user.save()
        media.media_likers.add(liker_user)
        media_liker_list.append(liker_user)

    media_comments = cl.media_comments(media_pk, 100)
    media_comment_list = []

    for media_comment in media_comments:
        media_commenter = convert_shortuser(media_comment.user, True)
        media_commenter.save()
        comment = convert_comment(media_comment)
        comment.save()
        media.media_comments.add(comment)
        media_comment_list.append(comment)

    return media_liker_list, media_comment_list
