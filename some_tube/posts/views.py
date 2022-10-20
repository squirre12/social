from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    latest = list(Post
                  .objects
                  .order_by("-pub_date")[:10]
                  .select_related("author"))
    return render(request, "index.html", {"posts": latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all().order_by("-pub_date")[:10]
    context = {"group": group, "posts": posts}
    return render(request, "group.html", context)
