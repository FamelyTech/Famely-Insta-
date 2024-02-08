from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('media/<str:media_pk>/', views.media_detail, name='media_detail'),
    path('account/<str:user_name>/', views.account_detail, name='account_detail'),
    path('error/', views.error_detail, name='error_detail'),
    path('create_jalodei_user/', views.create_jalodei_user, name='create_jalodei_user')
]
