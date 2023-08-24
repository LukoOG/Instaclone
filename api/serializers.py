from rest_framework import serializers
from user.models import *

# class MessageSerializer():
#     class Meta:
#         model = Message
#         fields = '__all__'

# class DMSerializer():
#     pass


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

        fields = ('message', 'media')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('message', )


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    def get_profile_pic(self, obj):
        return obj.profile.profile_pic.url if obj.profile.profile_pic else None

    def get_profile(self, obj):
        return obj.profile.user.username

    class Meta:
        model = Comment
        fields = ('id', 'profile', 'message', 'profile_pic')


class PostSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    def get_profile_pic(self, obj):
        return obj.profile.profile_pic.url if obj.profile.profile_pic else None

    def get_profile(self, obj):
        return obj.profile.user.username

    class Meta:
        model = Post
        fields = ('id', 'profile', 'date', 'message', 'media', 'profile_pic',
                  'like')


class DMMessageSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    profile_pic = serializers.SerializerMethodField()

    def get_profile_pic(self, obj):
        print(obj.sender.profile_pic)
        return obj.sender.profile_pic.url if obj.sender.profile_pic else None

    def get_profile(self, obj):
        return obj.sender.user.username

    class Meta:
        model = DMMessage
        fields = ('message', 'profile_pic', 'profile', 'sender', 'date')


class CreateDMMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMMessage
        fields = ('message',)
