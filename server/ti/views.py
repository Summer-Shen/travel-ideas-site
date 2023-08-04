from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Idea
from .serializers import IdeaSearchItemSerializer


# Create your views here.

@api_view(["GET"])
def search_ideas(request):
    query = request.GET.get("q", "")
    matched_ideas = Idea.objects.filter(title__icontains=query)
    matched_ideas = matched_ideas.annotate(comments_count=Count("comments"))
    serializer = IdeaSearchItemSerializer(matched_ideas, many=True)
    return Response(serializer.data)
