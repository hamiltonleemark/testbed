from django.conf.urls import patterns, url
from . import index 

urlpatterns = patterns(
  "product",
  url(r"^$", index.view),
  url(r"^(?P<pid>[\d]+)", index.view_product)
)
