from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from services.core.constants.error import FILE_ALREADY_EXISTS
from services.core.serializers.file import FileSerializer, CreateFileSerializer

from services.core.models import File
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
    serializer_class = FileSerializer

    def post(self, request):
        serializer = CreateFileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            uploaded_file = request.FILES.get('file')
            file_name = uploaded_file.name
            file_size = uploaded_file.size

            user = request.user
            check_file = File.objects.filter(name=file_name, user_id=user.id, directory=data.get('directory'))

            if len(check_file) > 0:
                raise WrapperException(FILE_ALREADY_EXISTS)
            else:
                data['user'] = user
                data['size'] = convert_bytes_to_human_readable(file_size)

                file = File.objects.create(**data)
                return Response(FileSerializer(file).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

