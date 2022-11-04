from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import NewPost
from .models import Post, Group


def index(request):
    latest = Post.objects.order_by("-pub_date").select_related("author").all()
    paginator = Paginator(latest, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"posts": latest, "page": page, "paginator": paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by("-pub_date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {"group": group, "posts": posts, "paginator": paginator, "page": page}
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


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post = user.posts.all().order_by("-pub_date")
    paginator = Paginator(post, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {"author": user, "page": page, "paginator": paginator}
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post.html', {"post": post, "author": user})


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect(f'/{author.username}/{post_id}')
    if request.method == 'POST':
        edit_form = NewPost(request.POST, instance=post)
        if edit_form.is_valid():
            post = edit_form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(f'/{author.username}/{post_id}')
    edit_form = NewPost(instance=post)
    return render(request, 'new_post.html', {"form": edit_form})
