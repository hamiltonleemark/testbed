from django.conf.urls import patterns, url
from . import testsuites

urlpatterns = patterns(
  "branch",
  url(r"testsuites/(?P<pid>[\d]+)", testsuites.index.view)
)
