from rest_framework import serializers

from services.core.models import File, Directory


class FileSerializer(serializers.ModelSerializer):
    # size = serializers.CharField()
    # name = serializers.CharField(max_length=255)
    # file_type = serializers.SerializerMethodField()
    # since_added = serializers.SerializerMethodField()
    # file = serializers.FileField()

    class Meta:
        model = File
        fields = '__all__'

    #
    # def get_file_type(self, obj):
    #     filename = obj.name
    #     return filename.split('.')[-1]

    def get_since_added(self, obj):
        date_added = obj.date_created
        return date_added

    def create(self, validated_data):
        return File.objects.create(**validated_data)


class CreateFileSerializer(serializers.Serializer):
    directory = serializers.PrimaryKeyRelatedField(
        queryset=Directory.objects.all(), write_only=True, required=False
    )
    file = serializers.FileField()

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        return File.objects.create(**validated_data)
