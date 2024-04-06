from django.shortcuts import render,get_object_or_404,redirect
from django.utils.timezone import now
from .models import Post, Tags, Category, Comment, PostPhoto,Profile
from django.db.models import Q
from .forms import PostForm, SubscribeForm, CommentForm, ProfileUpdateForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    posts=Post.objects.all().order_by("-published_date")
    paginator=Paginator(posts,2)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    tags = Tags.objects.all()
    comments = Comment.objects.all()
    context = {"posts": posts, "tags": tags,"comments": comments}
    context.update(get_categories())
    return render(request, 'blog/index.html',context)

def get_categories():
    all=Category.objects.all()
    count=all.count()
    half=count/2+count % 2
    return {'cats1':all[:half],'cats2':all[half:]}

def post(request,title=None):
    post=get_object_or_404(Post,title=title)
    imgs=PostPhoto.objects.filter(post=post)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post', title=title)
    else:
        form = CommentForm()
    context = {"post": post, "imgs":imgs,"form": form, "comments": comments}
    context.update(get_categories())
    return render(request, 'blog/post.html',context)

def about(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/about.html',context)

def contact(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/contact.html',context)

def category(request,name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)

def tag(request,name=None):
    category = get_object_or_404(Category, name=name)
    posts =Post.objects.filter(category=category).order_by("-published_date")
    context = {"posts":posts,"category": category}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)
def search(request):
    query=request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)

def subscribe(request):
    subMessage = None
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            subMessage = "You're subscriber!"
            form = SubscribeForm()
    else:
        form = SubscribeForm()
    return render(request, 'blog/base.html', {'form': form, 'subMessage': subMessage})

@login_required
def create(request):
    if request.method == 'POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date=now()
            post.user=request.user
            post.save()
            return index(request)
    form=PostForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/create.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    return render(request, 'blog/profile.html', {'user': request.user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'blog/update_profile.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/registration_user.html', {'form': form})

def add_comment_to_post(request, title):
    post = get_object_or_404(Post, title=title)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.username
            comment.save()
            return redirect('post', title=title)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

