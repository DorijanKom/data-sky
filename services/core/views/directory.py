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

    def delete(self, pk):
        try:
            Directory.objects.filter(id=pk).delete()
            return Response({"Success": "Directory deleted"}, status=status.HTTP_200_OK)
        except Directory.DoesNotExist:
            return Response({"Error": Directory.DoesNotExist}, status=status.HTTP_400_BAD_REQUEST)


class ListDirectoryContentsView(GenericAPIView):
    authentication_classes = [SessionAuthentication]

    def get_directory_contents(self, directory):
        # Recursively retrieve the contents of a directory
        contents = []

        subdirectories = Directory.objects.filter(parent_directory=directory)
        print(subdirectories)
        for subdirectory in subdirectories:
            contents.append({
                'type': 'directory',
                'name': subdirectory.name,
                'id': subdirectory.id,
                'contents': self.get_directory_contents(subdirectory)
            })

        files = File.objects.filter(directory_id=directory.id)
        print(files)
        for file in files:
            print(file.__dict__)
            contents.append({
                'type': 'file',
                'name': file.name,
                'id': file.id,
                'user_id': file.user_id,
                'date_created': file.date_created
            })
        return contents

    def get(self, request, pk):

        user = request.user

        directory = get_object_or_404(Directory, id=pk, user=user)

        # Get the contents of the directory
        contents = self.get_directory_contents(directory)

        print(contents)

        return Response(data=contents, status=status.HTTP_200_OK)
