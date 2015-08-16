from django.conf.urls import patterns, url
from . import index 

urlpatterns = patterns(
  "products",
  url(r"^$", index.view)
)
