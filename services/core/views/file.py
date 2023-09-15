from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from services.core.constants.error import FILE_ALREADY_EXISTS
from services.core.serializers.file import FileSerializer, CreateFileSerializer

from services.core.models import File, Directory
from services.core.utils.human_readable_bytes_util import convert_bytes_to_human_readable
from services.core.utils.wrapper_exception import WrapperException


class ListFileView(ListAPIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = FileSerializer

    def get_queryset(self):
        user = self.request.user
        query_set = File.objects.filter(user_id=user.id)
        return query_set


class FileView(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    parser_classes = [MultiPartParser]

    def post(self, request):
        user = request.user
        directory_id = request.data.get('directory')

        print(user.id)

        directory = get_object_or_404(Directory, id=directory_id, user=user)

        uploaded_file = request.data['file']
        file_name = uploaded_file.name
        file_size = uploaded_file.size

        file_data = {
            'user': user.id,
            'directory': directory.id,
            'name': file_name,
            'file': uploaded_file,
            'size': convert_bytes_to_human_readable(file_size),
        }

        print(file_data)

        file_serializer = FileSerializer(data=file_data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


