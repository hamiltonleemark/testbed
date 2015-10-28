from django.conf.urls import patterns, url
from .views import testsuites
from .views import tests

urlpatterns = patterns(
  "branch",
  url(r"tests/(?P<pid>[\d]+)", tests.index.view),
  url(r"testsuites/(?P<pid>[\d]+)", testsuites.index.view)
)
