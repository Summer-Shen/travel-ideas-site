from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Idea, User, Tag
from .serializers import IdeaSearchItemSerializer, UserSerializer, IdeaSerializer


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


@api_view(["POST"])
def create_idea(request):
    user_id = request.POST["user_id"]
    try:
        user = User.objects.get(id__exact=user_id)
    except User.DoesNotExist:
        return Response(
            "Please input valid user id.",
            status=status.HTTP_400_BAD_REQUEST
        )
    title = request.POST["title"]
    destination = request.POST["destination"]
    start_date_str = request.POST["start_date"]
    end_date_str = request.POST["end_date"]
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        if start_date > end_date:
            return Response(
                "End date should be the same or after start date.",
                status=status.HTTP_400_BAD_REQUEST
            )
    except ValueError:
        return Response(
            "Please input valid dates.",
            status=status.HTTP_400_BAD_REQUEST
        )
    # we pass tags as a string of tags with separators
    tags = request.POST["tags"].split(",")
    idea = Idea(
        user_id=user,
        title=title,
        destination=destination,
        start_date=start_date_str,
        end_date=end_date_str
    )
    idea.save()
    for tag_str in tags:
        tag = Tag(idea_id=idea, name=tag_str)
        tag.save()
    serializer = IdeaSerializer(idea, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
