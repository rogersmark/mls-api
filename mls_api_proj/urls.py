from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mls_api_proj.views.home', name='home'),
    # url(r'^mls_api_proj/', include('mls_api_proj.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('mls_api.urls')),
)
