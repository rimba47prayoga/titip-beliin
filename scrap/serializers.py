from urllib.parse import urlparse

from django.conf import settings
from rest_framework import serializers

from .models import ScrapModels
from .utils import Scrapper


class ScrapperSerializer(serializers.Serializer):

    url = serializers.URLField()

    def _is_detail_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc == 'www.amazon.com':
            # https://www.amazon.com/dp/B085K45C3S
            # After investigate, i found container element div with id="dp"
            # I think dp is stand for `detail product`
            detail_name = 'dp'
        else:
            # https://www.ebay.com/itm/294170428836
            detail_name = 'itm'
        try:
            is_detail_product = parsed_url.path.split('/')[1] == detail_name
        except IndexError:
            valid = False
        else:
            valid = is_detail_product
        return valid

    def validate(self, attrs):
        # execute default validate first
        attrs = super(ScrapperSerializer, self).validate(attrs)
        url = attrs.get('url')
        allowed_host = ['www.amazon.com', 'www.ebay.com']
        if urlparse(url).netloc not in allowed_host:
            raise serializers.ValidationError({
                'url': 'only supported scrapping for amazon & ebay'
            })

        if not self._is_detail_url(url):
            raise serializers.ValidationError({
                'url': f'{url} is not valid detail product.'
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
