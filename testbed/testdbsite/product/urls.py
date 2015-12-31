from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
  "product",
  url(r"^$", views.index),
  url(r"^(?P<pid>[\d]+)", views.index_product)
)
