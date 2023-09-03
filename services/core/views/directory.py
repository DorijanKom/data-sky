from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from services.core.models import File
from services.core.models.directory import Directory
from services.core.serializers.directory import DirectorySerializer


class DirectoryView(GenericAPIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = DirectorySerializer

    def post(self, request):
        serializer = DirectorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, id):
        try:
            Directory.objects.filter(id=id).delete()
            return Response({"Success": "Directory deleted"}, status=status.HTTP_200_OK)
        except Directory.DoesNotExist:
            return Response({"Error": Directory.DoesNotExist}, status=status.HTTP_400_BAD_REQUEST)


class ListDirectoryContentsView(GenericAPIView):
    authentication_classes = [SessionAuthentication]

    def get_directory_contents(self, directory):
        # Recursively retrieve the contents of a directory
        contents = []

        subdirectories = Directory.objects.filter(parent_directory=directory)
        for subdirectory in subdirectories:
            contents.append({
                'type': 'directory',
                'name': subdirectory.name,
                'id': subdirectory.id,
                'contents': self.get_directory_contents(subdirectory)
            })

        files = File.objects.filter(directory=directory)
        for file in files:
            contents.append({
                'type': 'file',
                'name': file.file.name,
                'id': file.id,
                'user_id': file.user_id.id,
                'date_created': file.date_created
            })

        return contents

    def get(self, request, directory_id):
        # Retrieve the starting directory
        directory = get_object_or_404(Directory, id=directory_id)

        # Get the contents of the directory
        contents = self.get_directory_contents(directory)

        return Response(data=contents, status=status.HTTP_200_OK)
