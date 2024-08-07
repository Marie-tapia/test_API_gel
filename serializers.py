from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    comments = serializers.ListField(
        child=serializers.CharField(max_length=50000)
    )
