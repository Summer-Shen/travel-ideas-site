from rest_framework import serializers

from .models import Idea, User, Comment


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
        fields = ["id", "title", "destination", "start_date", "end_date", "comments_count"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "idea_id", "user_id", "content", "created_at"]
