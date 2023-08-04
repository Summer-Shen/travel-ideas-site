from rest_framework import serializers

from .models import Idea


class IdeaSearchItemSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Idea
        fields = ["id", "title", "destination", "start_date", "end_date", "comments_count"]
