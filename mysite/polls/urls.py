from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^$',views.index,name='index'),
    url(r'^list/(?P<username>.*)$',views.list, name='listImages'),
    url(r'^image/(?P<filename>.*)$', views.getImage, name='getImage'),
]
