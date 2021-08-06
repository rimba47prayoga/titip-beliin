from urllib.parse import urlparse

from django.conf import settings
from rest_framework import serializers

from .models import ScrapModels
from .utils import Scrapper


class ScrapperSerializer(serializers.Serializer):

    url = serializers.URLField()

    def validate(self, attrs):
        # execute default validate first
        attrs = super(ScrapperSerializer, self).validate(attrs)
        url = attrs.get('url')
        allowed_host = ['www.amazon.com', 'www.ebay.com']
        if urlparse(url).netloc not in allowed_host:
            raise serializers.ValidationError({
                'url': 'only supported scrapping for amazon & ebay'
            })
        return attrs

    def scrap(self):
        url = self.validated_data.get('url')
        if settings.TESTING:
            instance = ScrapModels.objects.get(url=url)
            return instance.get_response
        scrapper = Scrapper(url)
        result = scrapper.scrap()
        try:
            ScrapModels.objects.get(url=url)
        except ScrapModels.DoesNotExist:
            ScrapModels.objects.create(
                url=url,
                response=result
            )
        return result
