# vim: tabstop=4 shiftwidth=4 softtabstop=4

from django.conf.urls import patterns, url

from .views import CustomizeInstanceView

V='feynapps.views'

urlpatterns = patterns(V,
    url(r'^$', CustomizeInstanceView.as_view(), name='index'),
)
