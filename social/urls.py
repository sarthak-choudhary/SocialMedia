from django.urls import path
from social import views

app_name = 'social'

urlpatterns=[

    path('home/',views.home,name='home'),
    
    path('profile/<int:id>/',views.profile,name='profile'),
    path('profile/update_profile',views.update_profile,name='update_profile'),
    path('myfeed/',views.myfeed,name='feed'),
    path('post/',views.new_post,name='post'),
    path('myfeed/post/<int:id>/comment',views.comments,name='postcomments'),
    path('myfeed/post/<int:id>',views.post_detail,name='post-detail'),
    path('home/post/<int:id>/',views.post_detail,name='post-detail'),
    path('home/post/<int:id>/edit',views.post_edit,name='postedit'),
    path('home/post/<int:id>/comment',views.comments,name='postcomments'),
    path('home/post/<int:id>/delete',views.post_delete,name='postdelete'),
    path('profile/<int:id>/follow/',views.user_follow,name='follow'),
    path('profile/<int:id>/unfollow/',views.user_unfollow,name='unfollow')
    ]
