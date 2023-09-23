import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from services.core.constants.error import FILE_ALREADY_EXISTS, FILE_DOES_NOT_EXIST
from services.core.serializers.file import FileSerializer

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

        if directory_id is None or directory_id == '':
            directory = get_object_or_404(Directory, name="/", parent_directory=None, user=user)
        else:
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

    def delete(self, request, pk):
        try:
            user = request.user

            file = get_object_or_404(File, id=pk, user=user)

            s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)

            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_key = file.name

            s3.delete_object(Bucket=bucket_name, Key=file_key)
            file.delete()

            return Response({'message': 'File deleted successfully'})
        except File.DoesNotExist:
            return Response({'error': FILE_DOES_NOT_EXIST})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk):
        try:
            user = request.user
            file = get_object_or_404(File, id=pk, user=user)

            s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL)

            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_key = file.name

            try:
                response = s3.generate_presigned_url('get_object',
                                                     Params={'Bucket': bucket_name,
                                                             'Key': file_key},
                                                     ExpiresIn=60)
                return Response(response)
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchKey':
                    return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except File.DoesNotExist:
            return Response({'error': str(File.DoesNotExist)}, status=status.HTTP_404_NOT_FOUND)
