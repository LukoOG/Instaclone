from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    #view functions
    path('', views.index),
    path('list-all-profiles', views.listProfile),  #just testing
    path('createpost', views.createPost),
    path('latestpost', views.latestPost),
    path('get-csrf-token', views.get_csrf_token),
    path('get-post/<str:pk>', views.getPost),
    path('like_unlike/<str:pk>', views.like_unlike),
    path('follow_unfollow/<str:pk>', views.follow_unfollow),
    path('createcomment/<str:pk>', views.createComment),
     path('deletecomment/<str:pk>', views.deleteComment),
    path('createdmmessage/<str:profile_name>', views.createDMMessage),
    path('dm_messages/<str:profile_name>', views.dm_messages),
]
