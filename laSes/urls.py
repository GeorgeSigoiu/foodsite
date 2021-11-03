from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
import webbrowser
from django.conf.urls.static import static
from django.conf import settings


def showHomePage(request):
    return render(request, "home.html")


def openLocationOnMaps(request, map_string):
    webbrowser.open('https://www.google.com/maps/place/' + map_string)
    return render(request, "home.html")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', showHomePage, name="home"),
    path('location/<str:map_string>/', openLocationOnMaps, name="location"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
