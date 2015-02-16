from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'tests.demo.views.index'),
)
