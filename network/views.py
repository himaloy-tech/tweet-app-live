from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Follower, Following
from django.core.paginator import Paginator

def index(request):
    posts = Post.objects.all().order_by('-datetime')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        follower = Follower(user=user)
        follower.save()
        following = Following(user=user)
        following.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='/login')
def post(request):
    if request.method == "POST":
        body = request.POST.get("message")
        user = request.user
        post = Post(body=body, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/post.html")

def profile(request, username):
    buttton = True
    check = False
    posts = Post.objects.filter(user__username=username).order_by('-datetime')
    follower_obj = Follower.objects.filter(user__username=username)
    following_obj = Following.objects.filter(user__username=username)
    for follower_count in follower_obj :
        follower_count = follower_count.user_following.all().count()

    for following_count in following_obj:
        following_count = following_count.user_following.all().count()
    if request.user.username == username:
        buttton = False
    else:
        check = Following.objects.filter(user = request.user, user_following__username=username).exists()
    return render(request, "network/profile.html", {
        "posts": posts,
        "username": username,
        "follower_count": follower_count,
        "following_count": following_count,
        "button":buttton,
        "check":check
        })

@login_required(login_url="/login")
def follow(request, username):
    current_user = request.user
    user = User.objects.get(username=username)

    following_obj = Following.objects.get(user=current_user)
    following_obj.user_following.add(user)

    follower_obj = Follower.objects.get(user=user)
    follower_obj.user_following.add(current_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
def unfollow(request, username):
    current_user = request.user
    user = User.objects.get(username=username)

    following_obj = Following.objects.get(user=current_user)
    following_obj.user_following.remove(user)

    follower_obj = Follower.objects.get(user=user)
    follower_obj.user_following.remove(current_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
def following(request):
    user_follower = Following.objects.get(user=request.user)
    posts = Post.objects.filter(user__in=user_follower.user_following.all()).order_by('-datetime')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": page_obj
    })

def obj(request, id):
    obj = Post.objects.get(id=id)
    body = obj.body
    return JsonResponse({"body": body})

def edit(request):
    if request.method == "POST":
        body = request.POST.get("textarea")
        id = request.POST.get("id")
        obj = Post.objects.get(id=id)
        obj.body = body
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def like(request, id, current_user):
    current_user = User.objects.get(username=current_user)
    post = Post.objects.get(id=id)
    post.like_users.add(current_user)
    post.like_num += 1
    post.save()
    return JsonResponse({"like_num": f"{post.like_num}"})

def unlike(request, id, current_user):
    current_user = User.objects.get(username=current_user)
    post = Post.objects.get(id=id)
    post.like_users.remove(current_user)
    post.like_num -= 1
    post.save()
    return JsonResponse({"like_num": f"{post.like_num}"})