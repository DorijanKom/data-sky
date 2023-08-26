from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from services.core.serializers.file import FileSerializer

from services.core.models import File


class ListFileView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = FileSerializer

    def get_queryset(self):
        user = self.request.user
        query_set = File.objects.filter(user_id=user.id)
        return query_set


class FileView(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = FileSerializer

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

