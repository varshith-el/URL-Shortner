from textwrap import shorten
from django.urls import path
from .views import home_page_view,shorten_url,redirect_short_url


urlpatterns = [
    path('home',home_page_view, name = 'home'),
    path('',home_page_view, name = 'home'),
    path('shorten',shorten_url, name = 'shorten'),
    path('<str:short_code>',redirect_short_url,name = 'redirection'),
    path('api/shorten/', shorten_url, name='api_shorten_url')

]