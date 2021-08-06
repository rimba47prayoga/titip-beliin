from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ScrapperSerializer


class ScrapperViews(APIView):

    def post(self, request):
        serializer = ScrapperSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.scrap())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
