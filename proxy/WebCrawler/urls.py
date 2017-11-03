from django.conf.urls import url,include
from .views import getJson
from .views import getMore

app_name = "WebCrawler"
urlpatterns = [
    url(r'^(?P<Type>[a-z A-Z]*)$', getJson),
    url(r'^119', getMore),
]