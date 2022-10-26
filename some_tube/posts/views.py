from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewPost
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


@login_required
def new_post(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('index')

    form = NewPost()
    return render(request, 'new_post.html', {"form": form})
