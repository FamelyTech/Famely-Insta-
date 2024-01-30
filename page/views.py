from django.http import HttpResponse
from django.template import loader
from .forms import InstagramForm
from .models import InstagramUser, JalodeiUser


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
        ig_user = ig_user[0]

        context.update({'active_user': ig_user,
                        'theme': jalodei_user.theme,
                        'saved_ig_users': jalodei_user.saved_users.all()})

        return HttpResponse(template.render(context, request))

    except Exception as e:
        template = loader.get_template('registration/login.html')
        return HttpResponse(template.render({}, request))
