from django.urls import path
from .views import ScrapperViews


urlpatterns = [
    path("scrap", ScrapperViews.as_view(), name='scrap')
]
