from rest_framework import serializers

from services.core.constants.error import DIRECTORY_ALREADY_EXISTS, DIRECTORY_DOES_NOT_BELONG_TO_USER
from services.core.models.directory import Directory
from services.core.utils.wrapper_exception import WrapperException


class DirectorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    since_added = serializers.SerializerMethodField()
    parent_directory = serializers.PrimaryKeyRelatedField(
        queryset=Directory.objects.all(), write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Directory
        fields = ['name']

    def get_since_added(self, obj):
        date_added = obj.date_created
        return date_added

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        parent_directory = validated_data['parent_directory']

        print(parent_directory)

        if parent_directory is None or parent_directory == '':
            root_directory = Directory.objects.filter(name='/', user=user, parent_directory=None).first()
            if root_directory:
                validated_data['parent_directory'] = root_directory
                print(validated_data['parent_directory'])

        if parent_directory:
            if parent_directory.user != user:
                raise WrapperException(DIRECTORY_DOES_NOT_BELONG_TO_USER)

        directory = Directory.objects.filter(name=validated_data.get('name'), user=user,
                                             parent_directory=validated_data.get('parent_directory'))
        if len(directory) > 0:
            raise WrapperException(DIRECTORY_ALREADY_EXISTS)
        else:
            return Directory.objects.create(**validated_data)


class DirectoryContentSerializer(serializers.Serializer):
    type = serializers.CharField()
    name = serializers.CharField()
    id = serializers.IntegerField()
    contents = serializers.ListField(child=serializers.DictField(), required=False)
    user_id = serializers.IntegerField(required=False)
    date_created = serializers.DateTimeField(required=False)
    size = serializers.CharField(required=False)
