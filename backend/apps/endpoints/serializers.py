from rest_framework import serializers
from apps.endpoints.models import *
from django.contrib.auth.models import User

# Authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields

class DL_CommentSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only = True)
    def get_current_status(self, dlcomment):
        return DL_CommentStatus.objects.filter(parent_dl_comment=dlcomment).latest("created_at").status

    class Meta:
        model = DL_Comment
        read_only_fields = ('id', "name", "description", "code", "version",
                            "owner", "created_at", "parent_endpoint", "current_status")
        fields = read_only_fields

class DL_CommentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DL_CommentStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_by", "created_at", "parent_dl_comment")

class DL_CommentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DL_CommentRequest
        read_only_fields = ("id", "input_data", "full_response", "response", "created_at", 
                            "parent_dl_comment")
        fields = ("id", "input_data", "full_response", "response", "created_at", 
                            "parent_dl_comment", "feedback")
