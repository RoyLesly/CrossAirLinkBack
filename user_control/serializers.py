from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from user_control.models import (CustomUser, UserProfile, CompanyProfile, ROLE_CHOICES, UserActivities)


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = "__all__"
        dept = 1


class PermissionSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(read_only=True)

    class Meta:
        model = Permission
        fields = "__all__"
        dept = 1


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = "__all__"
        dept = 1


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    role = serializers.ChoiceField(ROLE_CHOICES)


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    role = serializers.ChoiceField(ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        exclude = ("password",)
        # fields = "__all__"
        dept = 1


class LoginSerialiser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False)
    is_new_user = serializers.BooleanField(default=False, required=False)


class LogoutSerialiser(serializers.Serializer):
    user_id = serializers.CharField(required=True)


class AssignGroupsToUserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=Group.objects.all(), required=True)

    class Meta:
        model = CustomUser
        fields = ("__all__")


class AssignPermissionsToGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=Permission.objects.all(), required=True)

    class Meta:
        model = Group
        fields = ("__all__")


class CreatePasswordUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("password",)


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
        dept = 1


class GetUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    groups = GroupSerializer(read_only=True, many=True)
    user_permissions = PermissionSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ("__all__")


class UserActivitiesSerializer(serializers.Serializer):

    class Meta:
        model = UserActivities
        fields = ("__all__")


class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = ("__all__")
