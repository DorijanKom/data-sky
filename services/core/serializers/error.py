from rest_framework import serializers


class InnerErrorSerializer(serializers.Serializer):
    error = serializers.CharField(required=True)
    reason = serializers.CharField(required=True)
    namespace = serializers.CharField(required=False)


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField(required=True)
    reason = serializers.CharField(required=True)
    stack = InnerErrorSerializer(many=True, read_only=True)