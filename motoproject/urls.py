from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from . import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns (
    path('', views.main, name='main'),
    path("cerca/", views.cerca, name="cerca"),
    path('useri/', include('useri.urls')),
    path('blog/', include('blog.urls')),
    path('galleria/', include('galleria.urls')),
    path('ospite/', include('ospite.urls')),
    path('itinerario/', include('itinerario.urls'), verbose_name='itinerari'),
    path('evento/', include('evento.urls'), verbose_name='eventi'),
    path('novita/', include('novita.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

