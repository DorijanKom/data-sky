from rest_framework import serializers

from services.core.models import File


class FileSerializer(serializers.Serializer):
    size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()
    since_added = serializers.SerializerMethodField()
    
    class Meta:
        model = File
        fields = '__all__'

    def get_size(self, obj):
        file_size = ''
        if obj.file and hasattr(obj.file, 'size'):
            file_size = obj.file.size
        return file_size

    def get_name(self, obj):
        file_name = ''
        if obj.file and hasattr(obj.file, 'name'):
            file_name = obj.file.name
        return file_name

    def get_file_type(self, obj):
        filename = obj.file.name
        return filename.split('.')[-1]

    def get_since_added(self, obj):
        date_added = obj.file.date_created
        return date_added