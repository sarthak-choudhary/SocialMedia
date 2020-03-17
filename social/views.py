from django.shortcuts import render,get_object_or_404

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from social.forms import ProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings


from django.urls import reverse

from .forms import CommentForm,NewPostForm
from .models import Post
from .models import Comment


from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def new_post(request):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            post = Post.objects.create(title=title, message=content, author=user)

            #subject = f"{user.username} added a New Post"

            #from_email = settings.DEFAULT_FROM_EMAIL
            #to_email = ['csarthak76@gmail.com']

            #message = 'TITLE: {0}\nCONTENT:{1}'.format(title,content)

            #send_mail(subject,message,from_email,to_email,fail_silently=False)
            return redirect(reverse('social:home'))
    else:

        form = NewPostForm()

    return render(request, 'post.html', {'form': form})

def post_detail(request,id):
    post = get_object_or_404(Post,id=id)
    context = {
        'post':post,
        'title':post.title,
        'content':post.message,
        'author': post.author,
        'date_posted': post.created_at,
        'comments': post.comment_set.all(),
        'num_comments':post.comment_set.count()

    }
    return render(request,'postinfo.html',context=context)

def post_edit(request,id):
    post = get_object_or_404(Post,id=id)

    if post.author == request.user:
        if request.method == 'POST':
            form = NewPostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                post.title = title
                post.message = content
                post.save()
                return redirect('social:post-detail',id=id)
        else:
            form = NewPostForm({'title':post.title,'content':post.message})
        return render(request,'postedit.html',context={'title':'Edit Post','form':form})

def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('social:home')
    
    else:
        return redirect('home')
    return render(request,'postdelete.html',{'post': post})

def home(request):
    user = request.user
    following = user.profile.follows.all()
    
    context= {'post_records' : Post.objects.all()}
    return render(request,'home.html',context= {'post_records': Post.objects.all()})

def myfeed(request):
    user = request.user
    following = user.profile.follows.all()
    post_records = []
    # for post in Post.objects.all():
    #     if post.author in following:
    #         post_records.append(post)

    for profile in following:
        for post in profile.user.posts.all():
            post_records.append(post)

    print(post_records)

    context = {'post_records' : post_records}
    return render(request,'feed.html',context=context)    

    
def comments(request,id):
    
    user = request.user
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment(comment=form.cleaned_data['content'], author=user, post=post)
            comment.save()
            return redirect('social:post-detail', id=post.id)
            
    else:
            form = CommentForm()
    return render(request, 'comments.html', context={'form':form})
        
def profile(request,id):
    user = get_object_or_404(User,id=id)
    users = User.objects.all()

    context = {
        'user': user,
        'users' : users,
        'username': user.username,
        'name' :f'{user.profile.first_name} {user.profile.last_name}',
        'about': user.profile.about,
        'profile_pic' : user.profile.profile_pic,
        'birthdate':f'{user.profile.birthdate.strftime("%d-%m-%y")}',
        'tot_followers' : len(user.profile.followers.all()),
        'tot_following' : len(user.profile.follows.all())

    }
    return render(request,'profile.html',context=context)

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            about = form.cleaned_data['about']
            birthdate = form.cleaned_data['birthdate']
            profile_pic = request.FILES['profile_pic']
            user.profile.first_name = first_name
            user.profile.last_name = last_name
            user.profile.birthdate = birthdate
            user.profile.about = about
            user.profile.profile_pic = profile_pic
            user.save()
            return redirect('social:profile', id=user.id)
    else:
        form = ProfileUpdateForm({'first_name':user.profile.first_name,
                                'last_name' :user.profile.last_name,
                                'birthdate' :user.profile.birthdate,
                                'about': user.profile.about,
                                'profile_pic':user.profile.profile_pic})
    return render(request,'update_profile.html',context={'title':'Update Profile','form' : form})

def user_follow(request,id):
    user_follow = get_object_or_404(User,id=id)
    follower = request.user

    if follower.profile not in user_follow.profile.followers.all():
        user_follow.profile.followers.add(follower.profile)
        user_follow.save()

    return redirect('social:profile',id=request.user.id)

def user_unfollow(request,id):
    user_unfollow = get_object_or_404(User,id=id)
    unfollower = request.user
    if unfollower.profile in user_unfollow.profile.followers.all():
        user_unfollow.profile.followers.remove(unfollower.profile)
        user_unfollow.save()
    
    return redirect('social:profile',id=request.user.id)
