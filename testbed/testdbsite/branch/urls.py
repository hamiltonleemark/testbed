from django.conf.urls import patterns, url
from .views import tests

urlpatterns = patterns(
  "branch",
  url(r"tests/(?P<pid>[\d]+)", tests.index.view),
)
