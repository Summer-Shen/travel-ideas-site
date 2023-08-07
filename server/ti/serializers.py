from rest_framework import serializers

from .models import Idea, User, Comment, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email"]


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ["id", "title", "destination", "start_date", "end_date"]


class IdeaSearchItemSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Idea
        fields = ["id", "title", "destination", "start_date", "end_date", "comments_count", "user_id"]


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user_id.name", read_only=True)
    
    class Meta:
        model = Comment
        fields = ["id", "idea_id", "user_id", "content", "created_at", "user_name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "idea_id", "name"]
