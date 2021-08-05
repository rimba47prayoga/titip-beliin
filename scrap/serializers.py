from rest_framework import serializers


class ScrapperSerializer(serializers.Serializer):

    url = serializers.URLField()
