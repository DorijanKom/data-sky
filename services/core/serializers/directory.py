from rest_framework import serializers

from services.core.models import Directory


class DirectorySerializer(serializers.Serializer):
    size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    since_added = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = "__all__"

    def get_size(self, obj):
        directory_size = ''
        if obj.directory and hasattr(obj.directory, 'size'):
            directory_size = obj.directory.size
        return directory_size

    def get_name(self, obj):
        directory_name = ''
        if obj.directory and hasattr(obj.directory, 'name'):
            directory_name = obj.directory.name
        return directory_name

    def get_since_added(self, obj):
        date_added = obj.directory.date_created
        return date_added
