from django import forms


class InstagramForm(forms.Form):
    account_name = forms.CharField(max_length=100)
    media_id = forms.CharField(max_length=100)


class JalodeiUserConfiguration(forms.Form):
    instagram_user = forms.CharField(label='Instagram Username', max_length=100)
    instagram_password = forms.CharField(label='Password', widget=forms.PasswordInput)
    proxy = forms.CharField(label='Proxy (address:port)', max_length=100)
