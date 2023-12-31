import json
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Count
from django.utils.html import escape
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Idea, User, Tag, Comment
from .serializers import IdeaSearchItemSerializer, UserSerializer, IdeaSerializer, CommentSerializer, TagSerializer


# Create your views here.

@api_view(["POST"])
def register(request):
    name = request.POST.get("name")
    # data validation
    if len(name) > 20:
        return Response(
            "The maximum length of the user name is 20 characters.",
            status=status.HTTP_400_BAD_REQUEST
        )
    email = request.POST.get("email")
    try:
        validate_email(email)
    except ValidationError:
        return Response("Please input valid email address.", status=status.HTTP_400_BAD_REQUEST)
    password = request.POST.get("password")
    hashed_password = make_password(password)
    user = User(name=name, email=email, password=hashed_password)
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def login(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        user = User.objects.get(email__exact=email)
    except User.DoesNotExist:
        return Response(
            "Incorrect email, please try again.",
            status=status.HTTP_400_BAD_REQUEST
        )
    encoded = user.password
    if check_password(password, encoded):
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response("Incorrect email or password, please try again.", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_idea(request):
    user_id = request.POST.get("user_id")
    try:
        user = User.objects.get(id__exact=user_id)
    except User.DoesNotExist:
        return Response(
            "Please input valid user id.",
            status=status.HTTP_400_BAD_REQUEST
        )
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    try:
        start_date = datetime.date(datetime.fromisoformat(start_date))
        end_date = datetime.date(datetime.fromisoformat(end_date))
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
    # we pass tags as json
    tags = json.loads(request.POST.get('tags'))
    idea = Idea(
        user_id=user,
        title=request.POST.get("title"),
        destination=request.POST.get("destination"),
        start_date=start_date,
        end_date=end_date
    )
    idea.save()
    for tag in tags:
        Tag(idea_id=idea, name=tag).save()
    serializer = IdeaSerializer(idea, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def delete_idea(request):
    idea_id = request.POST.get("idea_id")
    try:
        idea = Idea.objects.get(id__exact=idea_id)
    except Idea.DoesNotExist:
        return Response(
            "Please input valid idea id.",
            status=status.HTTP_400_BAD_REQUEST
        )
    idea.delete()
    return Response("Idea deleted.", status=status.HTTP_200_OK)


@api_view(["POST"])
def modify_idea(request):
    idea_id = request.POST.get("id")
    try:
        idea = Idea.objects.get(id__exact=idea_id)
    except Idea.DoesNotExist:
        return Response(
            "Please input valid idea id.",
            status=status.HTTP_400_BAD_REQUEST
        )
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")
    try:
        start_date = datetime.date(datetime.fromisoformat(start_date))
        end_date = datetime.date(datetime.fromisoformat(end_date))
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
    idea.title = request.POST.get("title")
    idea.destination = request.POST.get("destination")
    idea.start_date = start_date
    idea.end_date = end_date
    idea.save()
    
    # update tags by first deleting the existing ones
    Tag.objects.filter(idea_id__exact=idea).delete()
    # we pass tags as json
    tags = json.loads(request.POST.get('tags'))
    for tag in tags:
        Tag(idea_id=idea, name=tag).save()
    serializer = IdeaSerializer(idea, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_idea_by_id(request):
    query = request.GET.get("q", "")
    try:
        idea = Idea.objects.get(id__exact=query)
    except Idea.DoesNotExist:
        return Response(
            "Please input valid idea id.",
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = IdeaSerializer(idea, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_tags_by_idea(request):
    query = request.GET.get("q", "")
    tags = Tag.objects.filter(idea_id=query)
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)


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


@api_view(["POST"])
def create_comment(request):
    idea_id = request.POST.get("idea_id")
    try:
        idea = Idea.objects.get(id__exact=idea_id)
    except Idea.DoesNotExist:
        return Response(
            "Please input valid idea id.",
            status=status.HTTP_400_BAD_REQUEST
        )
    user_id = request.POST.get("user_id")
    try:
        user = User.objects.get(id__exact=user_id)
    except User.DoesNotExist:
        return Response(
            "Please input valid user id.",
            status=status.HTTP_400_BAD_REQUEST
        )
    content = request.POST.get("content")
    # escape content of the comment
    content = escape(content)
    # data validation
    if len(content) > 255:
        return Response(
            "The maximum length of a comment is 255 characters.",
            status=status.HTTP_400_BAD_REQUEST
        )
    comment = Comment(idea_id=idea, user_id=user, content=content)
    comment.save()
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_comments_by_idea(request):
    query = request.GET.get("q", "")
    matched_comments = Comment.objects.filter(idea_id=query).order_by('-created_at')
    serializer = CommentSerializer(matched_comments, many=True)
    return Response(serializer.data)
