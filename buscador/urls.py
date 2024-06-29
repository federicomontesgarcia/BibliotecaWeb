from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    #path('', views.librosBuscados, name='librosBuscados'),
    path('', views.LibrosViews.as_view(), name='librosBuscados'),
]