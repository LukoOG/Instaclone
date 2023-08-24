from multiprocessing import context
from pydoc_data.topics import topics
from re import template
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from .forms import *


# Create your views here.
def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('pass')
        try:
            user = User.objects.get(username)
        except:
            messages.error(request, 'The User was not found bro')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:home')
        else:
            print("Sorry boy. You are not a user")

    context = {'page': page}
    return render(request, 'user/login_register.html', context)


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:login')
        else:
            print('why')
    context = {'page': page, 'form': form}
    return render(request, 'user/login_register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('user:home')


def createPost(request):
    profile = request.user.profile
    user_profile = request.user.profile
    print(request.user)
    profiles = Profile.objects.exclude(user=request.user)
    post = user_profile.profile_post
    all_post = Post.objects.filter(
        profile__in=request.user.profile.follows.all()).order_by("-date")
    comment = Comment.objects.all()

    total_followers = user_profile.follows.exclude(user=request.user).count()
    total_followed = user_profile.followed_by.exclude(
        user=request.user).count()
    total_post = post.count()

    formie = PostForm(instance=request.user)
    if request.method == 'POST':
        formie = PostForm(request.POST, request.FILES)
        if formie.is_valid():
            post = formie.save(commit=False)
            post.profile = request.user.profile
            post.save()
            return redirect('user:home')
    context = {
        'user_profile': user_profile,
        'all_post': all_post,
        'profiles': profiles,
        'total_followers': total_followers,
        'total_followed': total_followed,
        'total_post': total_post,
        'comment': comment,
        'formie': formie
    }
    return render(request, 'user/postform.html', context)


def updatePost(request, pk):
    formay = Post.objects.get(id=pk)
    if formay.profile != request.user.profile:
        # return redirect('user:home')
        messages.info(
            request, 'You are not authorized to make changes to this Post!!!')
        return redirect('user:postpage', formay.id)
    else:
        formie = PostForm(instance=formay)
        if request.method == 'POST':
            formie = PostForm(request.POST, request.FILES, instance=formay)
            if formie.is_valid():
                formie.save()
                return redirect('user:home')
    context = {'formie': formie}
    return render(request, 'user/createpost.html', context)


##Until someone knows how to use javascript, reactjs or the rest framework
##gotta pass in the page url to the function, so it refreshes the page accordingly

##deprecated
# def follow_unfollow(request, profile):
#     user_profile = request.user.profile
#     if request.method == 'POST':

#         action = request.POST.get('follow')
#         if action == 'follow':
#             user_profile.follows.add(profile)
#         elif action == 'unfollow':
#             user_profile.follows.remove(profile)
#         else:
#             print('nope')

# def like_unlike(request, post, path):

#     user_profile = request.user.profile
#     if request.method == 'POST':
#         action = request.POST.get('like')
#         if action == 'like':
#             post.like.add(user_profile)
#         elif action == 'unlike':
#             post.like.remove(user_profile)
#     likes = post.like.count()
#     return redirect(path)


# def comment__(request, post):
#     user_profile = request.user.profile
#     message = request.POST.get('comment')
#     if message:
#         if request.method == 'POST':
#             commie = Comment.objects.create(post=post,
#                                             profile=user_profile,
#                                             message=message)
#             return redirect('user:postpage', post.id)
#     else:
#         pass


def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if post.profile != request.user.profile:
        # return redirect('user:home')
        messages.info(request, 'You are not authorized to delete this Post!!!')
        return redirect('user:home')
    else:
        post.delete()
        return redirect('user:home')


def deleteComment(request, pk):
    # post = Post.objects.get(id=pk)
    commie = Comment.objects.get(id=pk)
    post = commie.post
    if commie.profile != request.user.profile:
        # return redirect('user:home')
        messages.info(request, 'You are not authorized to delete this Post!!!')
        return redirect('user:home')
    else:
        commie.delete()
        return redirect('user:postpage', post.id)
    # context
    # return render(request, 'user/postpage.html')
