"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ti import views

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/users/register", views.register),
    path("api/users/login", views.login),
    path("api/ideas/create", views.create_idea),
    path("api/ideas/delete", views.delete_idea),
    path("api/ideas/modify", views.modify_idea),
    path("api/ideas/search_by_dest", views.search_ideas_by_destination),
    path("api/ideas/search_by_tag", views.search_ideas_by_tag),
    path("api/comments/create", views.create_comment),
    path("api/comments/get_by_idea", views.get_comments_by_idea),
]
