from django.conf.urls import patterns, include, url
from yelp_zillow.views import home, search
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$'			   , home),
    url(r'^$'			   , home),
    url(r'^search/$'			   , search),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
urlpatterns += staticfiles_urlpatterns()