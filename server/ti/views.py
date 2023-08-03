from rest_framework import viewsets

from .models import Idea
from .serializers import IdeaSerializer


# Create your views here.

class IdeaView(viewsets.ModelViewSet):
    serializer_class = IdeaSerializer
    queryset = Idea.objects.all()
