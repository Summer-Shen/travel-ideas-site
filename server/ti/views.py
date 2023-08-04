from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Idea, User
from .serializers import IdeaSearchItemSerializer, UserSerializer


# Create your views here.

@api_view(["POST"])
def register(request):
    name = request.POST["name"]
    email = request.POST["email"]
    try:
        validate_email(email)
    except ValidationError:
        return Response("Please input valid email address.", status=status.HTTP_400_BAD_REQUEST)
    password = request.POST["password"]
    hashed_password = make_password(password)
    user = User(name=name, email=email, password=hashed_password)
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def login(request):
    email = request.POST["email"]
    password = request.POST["password"]
    user = User.objects.get(email__exact=email)
    encoded = user.password
    if check_password(password, encoded):
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Incorrect email or password, please try again.", status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def search_ideas_by_destination(request):
    query = request.GET.get("q", "")
    matched_ideas = Idea.objects.filter(destination__icontains=query)
    matched_ideas = matched_ideas.annotate(comments_count=Count("comments"))
    serializer = IdeaSearchItemSerializer(matched_ideas, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def search_ideas_by_tag(request):
    query = request.GET.get("q", "")
    matched_ideas = Idea.objects.filter(tags__name=query)
    matched_ideas = matched_ideas.annotate(comments_count=Count("comments"))
    serializer = IdeaSearchItemSerializer(matched_ideas, many=True)
    return Response(serializer.data)
