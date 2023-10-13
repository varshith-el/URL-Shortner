from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from urllib import response
from django.shortcuts import render, redirect
from django.http import HttpResponse,response
from .services import URLShortenerService
from .forms import shortenedURLForm
from .models import ShortenedURL
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home_page_view(request):
    form = shortenedURLForm()
    return render(request, 'home.html',{'form': form})


def redirect_short_url(request,short_code):
    original_url = cache.get(short_code)
    if original_url is None:
        # If it's not in the cache, get it from the database
        try:
            url_mapping = ShortenedURL.objects.get(short_url=short_code)
            original_url = url_mapping.original_url

            # Store it in the cache for future access, with the short_url as the key
            # The timeout parameter is optional. If not provided, 
            # it will use the default cache timeout.
            cache.set(short_code, original_url, timeout=60*60*24)  # Cache it for 24 hours
        except ShortenedURL.DoesNotExist:
            return HttpResponse('Short URL does not exist', status=404)
    print(original_url)
    return redirect(original_url, permanent = True)


@api_view(['GET','POST'])
def shorten_url(request):
    if request.method == 'POST':
        print(request.META)
        form = shortenedURLForm(request.POST or None)
        url = request.data.get('url') or None
        if form.is_valid() or url:
            original_url = url or form.cleaned_data['url']
            url_shortener = URLShortenerService()
            short_url = url_shortener.generate_short_url(original_url)
            ShortenedURL.objects.create(original_url=original_url, short_url=short_url)
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  # If the request was made via AJAX (i.e., through the API)
                return Response({"short_url": short_url}, status=status.HTTP_201_CREATED)
            else:  # If the request was made via a form submission (i.e., through the website)
                context = {'short_url': short_url}
                return render(request, 'shortened.html', context)
        else:
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return Response({"error": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return render(request, 'shorten.html', {'form': form})
    else:  # If it's a GET request
        form = shortenedURLForm()
        return render(request, 'shorten.html', {'form': form})
        '''
        return Response({"message": "Send a POST request to shorten a URL."}, status=status.HTTP_400_BAD_REQUEST)'''
    
'''
@api_view
def shorten_url(request):
    if request.method == 'POST':
        form = shortenedURLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['url']
            url_shortener = URLShortenerService()
            short_url = url_shortener.generate_short_url(original_url)
            ShortenedURL.objects.create(original_url = original_url, short_url = short_url)
            context = {'short_url':short_url}
            return render(request,'shortened.html', context)
    else:
        form = shortenedURLForm()
        return render(request, 'shorten.html',{'form': form})'''

