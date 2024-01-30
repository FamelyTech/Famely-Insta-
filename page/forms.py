from django import forms


class InstagramForm(forms.Form):
    account_name = forms.CharField(max_length=100)
    media_id = forms.CharField(max_length=100)
