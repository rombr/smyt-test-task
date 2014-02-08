from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^api/(?P<model_name>\w+)/(?P<object_id>\d+)/$', views.api_details,
                                                name='api_details'),
    url(r'^api/(?P<model_name>\w+)/$', views.api, name='api'),
)
