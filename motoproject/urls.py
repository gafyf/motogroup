from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),
]

urlpatterns += i18n_patterns (
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('weather/', include('weather.urls')),
    path('gallery/', include('gallery.urls')),
    path('guest/', include('guest.urls')),
    path('itinerary/', include('itinerary.urls')),
    path('event/', include('event.urls')),
    path('new/', include('new.urls')),
    path('chat/', include('chat.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


