from django.shortcuts import render
from django.shortcuts import get_object_or_404
#serializer import
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
#
from user.models import Profile, Post
from user.forms import *
from api.serializers import *


# Create your views here.
@api_view(['GET'])
def index(request):
    api_urls = {
        'list profiles': 'list-all-profiles',
        'create a poost': 'createpost',
        'get latest post': 'latestpost',
        'view a post': 'get-post',
        'get the csrf token': 'get-csrf-token'
    }  #just copying dennis's style

    return Response(api_urls)


@api_view(['GET'])
def listProfile(request):
    Profiles = Profile.objects.all()
    serializer = ProfileSerializer(Profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def latestPost(request):
    post = Post.objects.last()
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def like_unlike(request, pk):
    user_profile = request.user.profile
    post = Post.objects.get(id=pk)
    action = request.data.get('action')
    if action == 'like':
        post.like.add(user_profile)
    elif action == 'unlike':
        post.like.remove(user_profile)
    likes = post.like.count()
    return JsonResponse({'likes': likes, 'action': action})


@api_view(['POST'])
def follow_unfollow(request, pk):
    user_profile = request.user.profile
    profile = Profile.objects.get(id=pk)
    action = request.data.get('action')
    if action == 'follow':
        user_profile.follows.add(profile)
    elif action == 'unfollow':
        user_profile.follows.remove(profile)
    total_followers = profile.follows.exclude(id=profile.id).count()
    total_followed = profile.followed_by.exclude(id=profile.id).count()
    print(total_followers, total_followed)
    return JsonResponse({
        'action': action,
        'total_followed': total_followed,
        'total_followers': total_followers
    })


@csrf_exempt
@api_view(['POST', 'GET'])
#@permission_classes([IsAuthenticated])
def createPost(request):
    if request.method == 'POST':
        message = request.data.get('message')
        media = request.data.get('media')
        parser_classes = [MultiPartParser]
        data = request.data
        user_profile = request.user.profile
        form_serializer = PostCreateSerializer(data=data,
                                               context={'request': request})
        print('hmm', request.method)
        if form_serializer.is_valid():
            post = form_serializer.save(profile=request.user.profile)
            serializer = PostSerializer(instance=post)
            #return Response(serializer.data, status=201)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@csrf_exempt
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def createComment(request, pk):
    data = request.data
    print(data)
    user_profile = request.user.profile
    post = Post.objects.get(id=pk)
    form_serializer = CommentCreateSerializer(data=data)
    if form_serializer.is_valid():
        comment = form_serializer.save(profile=user_profile, post=post)
        serializer = CommentSerializer(instance=comment)
        return Response(serializer.data, status=201)
    return Response(form_serializer.errors, status=400)

@api_view(['POST'])
def deleteComment(request, pk):
    data = request.data
    print(data)
    user_profile = request.user.profile
    comment = Comment.objects.get(id=pk)
    comment.delete()
    if comment.profile != request.user.profile:
        return Response({'error':'unauthorized to perform this action'})
    

@csrf_exempt
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def createDMMessage(request, profile_name):
    user_profile = request.user.profile
    data = request.data
    dm = DMGroup.objects.filter(participants=user_profile).filter(
        participants__user__username=profile_name).get()
    form_serializer = CreateDMMessageSerializer(data=data)
    if form_serializer.is_valid():
        DMMessage = form_serializer.save(sender=user_profile, DM=dm)
        serializer = DMMessageSerializer(instance=DMMessage)
        print(serializer.data)
        return Response(serializer.data, status=201)
    return Response(form_serializer.errors, status=400)

@csrf_exempt
@api_view(['GET'])
def dm_messages(request, profile_name):
    user_profile = request.user.profile
    try:
        dm = DMGroup.objects.filter(participants=user_profile).filter(
            participants__user__username=profile_name).get()
    except DMGroup.DoesNotExist:
        dm = DMGroup.objects.create()
        dm.participants.add(user_profile)
        dm_profile = get_object_or_404(Profile, user__username=profile_name)
        dm.participants.add(dm_profile)

    dm_title = list(
        dm.participants.exclude(user=user_profile.user.id).values(
            'user__username', 'profile_pic'))
    dm_messages = dm.messages.order_by('date').values(
        'id', 'message', 'date', 'sender__user__username',
        'sender__profile_pic')
    messages = []
    for message in dm_messages:
        messages.append({
            'id': message['id'],
            'message': message['message'],
            'date': message['date'].strftime('%Y-%m-%dT%H:%M:%SZ'),
            'profile': message['sender__user__username'],
            'profile_pic': message['sender__profile_pic'],
        })
    data = {'dm_messages': messages}
    #print(messages)
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def get_csrf_token(request):
    print({'csrf_token': get_token(request)})
    return JsonResponse({'csrf_token': get_token(request)})