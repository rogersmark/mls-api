from django.conf.urls.defaults import url, patterns, include

from mls_api.api import router


urlpatterns = patterns('',
    url(r'', include(router.urls)),
)
