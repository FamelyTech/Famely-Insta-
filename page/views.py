from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .forms import InstagramForm
from .helpers.ai import (analyze_face, analyze_image, openai_analyze_comments)
from .helpers.converters import convert_comment, convert_shortuser, convert_facial_analysis
from .helpers.display import (get_media_display, get_usertag_display, get_top_hashtag_display,
                              get_user_display)
from .models import FacialAnalysis, InstagramMedia, InstagramUser, JalodeiUser


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

        jalodei_user = JalodeiUser.objects.get(user=request.user)
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
        template = loader.get_template('registration/login.html')
        return HttpResponse(template.render({}, request))


def account_detail(request, user_name):
    template = loader.get_template('insta/account_detail.html')
    jalodei_user = JalodeiUser.objects.get(user=request.user)

    try:
        user_display_info = get_user_display(request, user_name)
    except Exception as e:
        context = inst_error_context(e)
        return render(request, 'insta/error_detail.html', context)

    media_display_info = get_media_display(request, user_name)

    # recent_hashtag_display_info = get_recent_hashtag_display(request, user_name)

    top_hashtag_display_info = get_top_hashtag_display(request, user_name)

    usertag_display_info = get_usertag_display(request, user_name)

    context = {'user': user_display_info,
               'theme': jalodei_user.theme,
               'media_list': media_display_info,
               'top_hashtag_list': top_hashtag_display_info,
               'usertag_list': usertag_display_info}

    return HttpResponse(template.render(context, request))


def media_detail(request, media_pk):
    jalodei_user = JalodeiUser.objects.get(user=request.user)
    template = loader.get_template('insta/media_detail.html')
    media_likers, media_comments = get_media_details(request, media_pk)

    media = InstagramMedia.objects.get(media_id=media_pk)
    facial_analysis = []

    if media.thumbnail_url is not None:
        hume_response = analyze_image(media.thumbnail_url)
        media.hume_image_description = hume_response

        facial_analysis = analyze_face(hume_response)

        if facial_analysis != '':
            analysis = FacialAnalysis.objects.filter(media=media)
            if len(analysis) < 1:
                analysis = FacialAnalysis()
                analysis.media = media
                analysis.media_pk = media.media_id
            else:
                analysis = analysis[0]

            analysis = convert_facial_analysis(analysis, facial_analysis)
            analysis.save()

            for emotion in facial_analysis:
                emotion['score'] = f"{str(emotion['score'])[2:4]}.{str(emotion['score'])[4:7]}%"

    else:
        media.google_vision_image_description = None

        media.hume_image_description = None

    openai_comments_analysis = openai_analyze_comments(media_comments)
    media.openai_comments_description = openai_comments_analysis

    media.save()

    context = {'media_liker_list': media_likers,
               'theme': jalodei_user.theme,
               'media_comment_list': media_comments,
               'media_pk': media_pk,
               'facial_analysis': facial_analysis,
               'openai_comments_analysis': openai_comments_analysis}

    return HttpResponse(template.render(context, request))


def error_detail(request, context):
    template = loader.get_template('insta/error_detail.html')

    return HttpResponse(template.render(context, request))


def get_media_details(request, media_pk):
    request_user = JalodeiUser.objects.get(user=request.user)
    cl = inst_set_proxy(request_user.instagram_proxy)
    cl = inst_login_client(cl, request_user.instagram_username, request_user.instagram_password)
    media = InstagramMedia.objects.get(media_id=media_pk)

    # set update to True for 24 hour (or other time)
    update = False

    if update:
        media_likers = cl.media_likers(media_pk)
        media_liker_list = []

        for media_liker in media_likers:
            liker_user = convert_shortuser(media_liker)
            liker_user.save()
            media.media_likers.add(liker_user)
            media_liker_list.append(liker_user)

        media_comments = cl.media_comments(media_pk, 100)
        media_comment_list = []

        for media_comment in media_comments:
            media_commenter = convert_shortuser(media_comment.user)
            media_commenter.save()
            comment = convert_comment(media_comment)
            comment.save()
            media.media_comments.add(comment)
            media_comment_list.append(comment)

    else:
        media_liker_list = media.media_likers.all()
        media_comment_list = media.media_comments.all()

    return media_liker_list, media_comment_list
