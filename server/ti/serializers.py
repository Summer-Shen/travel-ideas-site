from rest_framework import serializers

from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ("id", "user_id", "title", "destination", "start_date", "end_date", "created_at", "modified_at")