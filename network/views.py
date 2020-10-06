from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json


from .models import User, Post, Profile, Like

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), label='')

def index(request):
    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/index.html", {'page': page})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        uname = request.POST["username"]
        username = uname.lower()
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
        uname = request.POST["username"]
        username = uname.lower()
        email = request.POST["email"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        image = request.POST["image"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        check = User.objects.filter(email=email)
        if check:
            return render(request, "network/register.html", {
                "message": "Email Id Exists. Please Login!"
            }) 
        # Attempt to create new user
        else:
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                if(image):
                    user.image = image
                else:
                    user.image = "https://i.pinimg.com/originals/0c/3b/3a/0c3b3adb1a7530892e55ef36d3be6cb8.png"
                user.save()
            except IntegrityError:
                return render(request, "network/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def create(request):
    if request.method =="POST":
        #post = Post(request.POST)
        user = request.user
        body = request.POST["body"]
        public = request.POST["visiblity"]
        post = Post.objects.create(user=user,body=body,public=public)
        post.save()
        return HttpResponseRedirect(reverse('index'))


    return render(request,"network/create.html",{
        
    })
@login_required(login_url='login')
def edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if(request.user==post.user):
        if request.method == 'POST':
            textarea = request.POST["body"]
            post.body = textarea
            post.edited = True
            post.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request,'network/edit.html',{
            'post' : post,
        })
    else:
        return render(request,'network/error.html')


@login_required(login_url='login')
def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        if(request.user==post.user):
            post.delete()
        return HttpResponseRedirect(reverse('index'))
@login_required(login_url='login')
@csrf_exempt
def like(request,post_id):
    user = request.user
    print(f"User is: {user.username}")
    # if request.method == 'GET':
    #     #post_id = request.GET['post_id']
    #     post = Post.objects.get(pk=post_id)
    #     if user in post.likes.all():
    #         post.likes.remove(user)
    #         like = Like.objects.get(post=post, user=user)
    #         like.delete()
    #     else:
    #         like = Like.objects.get_or_create(post=post, user=user)
    #         post.likes.add(user)
    #         post.save()
        
    #     return HttpResponseRedirect(reverse(index))
    post=Post.objects.get(pk=post_id)
    print(post)
    if request.method == "GET":
        return JsonResponse(post.serialize())
    # if request.method == "PUT":
    #     if user in post.likes.all():
    #         post.likes.remove(user)
    #         like = Like.objects.get(post=post, user=user)
    #         like.delete()
    #         print("like deleted")
    #     else:    
    #         like = Like.objects.get_or_create(post=post, user=user)
    #         post.likes.add(user)
    #         post.save()
    #         print("like saved")
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            # email.archived = data["archived"]
            if user in post.likes.all():
                post.likes.remove(user)
                like = Like.objects.get(post=post,user=user)
                like.delete
            else:
                like = Like.objects.get_or_create(post=post,user=user)
                post.likes.add(user)
                post.save()
                print("like saved")
        return JsonResponse(post.serialize())
    else:
        return JsonResponse({"error": "Error Encountered"}, status=400)
@csrf_exempt
@login_required(login_url='login')
def search(request):
    fdata = request.POST.copy()
    if not fdata:
        fdata = request.GET.copy()
    data = fdata.get('q')
    if(data):
        if(data==' ' or data == '   '):
            return HttpResponseRedirect(reverse(index))
        else:
            users = User.objects.all()
            token = False
            finallist = []
            searchmsg = "Matching User(s) Found"
            errmsg = "No Matching User Found"
            for user in users:
                fname = user.first_name
                lname = user.last_name
                if data.lower() in user.username or data.lower() in fname.lower() or data.lower() in lname.lower():
                    finallist.append(user)
                    token = True
            if token is True:
                return render(request, "network/search.html", {
                "entries": finallist,
                "msg": searchmsg,
                "token":token
            })
            else:
                return render(request, "network/search.html", {
                "msg": errmsg,
                "token":token
            })
    else:
        return HttpResponseRedirect(reverse(index))

@login_required(login_url='login')
def profile(request,username):
    user = get_object_or_404(User,username=username)
    posts = Post.objects.all().order_by('id').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if user: 
        follower = Profile.objects.filter(target=user)
        following = Profile.objects.filter(follower=user)
        follows = Profile.objects.filter(follower=request.user, target=user)
        followers = len(follower)
        followings = len(following)
        message = None
        if follows:
            follow_check = True
        else:
            follow_check = False
        print(follows)
        print(follow_check)
        return render(request,"network/profile.html",{
            "user": user,
            "page": page,
            'followers': followers,
            'following': following,
            'followings': followings,
            'followingcheck': follow_check,
            'message': message,
        })
    else:
        return render(request,'network/error.html')

@login_required(login_url='login')
def follow(request,username):
    user = get_object_or_404(User, username=username)
    following_each_other = Profile.objects.filter(follower=request.user, target=user)
    if not following_each_other:
        follow = Profile.objects.create(target=user, follower=request.user)
        follow.save()
        return HttpResponseRedirect(reverse('profile',args=(username,)))
    elif following_each_other:
        following_each_other.delete()
    return HttpResponseRedirect(reverse('profile',args=(username,)))

@login_required(login_url='login')
def following(request):
    follows = Profile.objects.filter(follower=request.user)
    posts = Post.objects.all().order_by('id').reverse()
    postlist = []
    for post in posts:
        for follower in follows:
            if follower.target == post.user:
                postlist.append(post) 
    if not follows:
        return render(request, 'network/follow.html', {'msg': "Looks Lonely Here... Lets start by Following People!!"})
    else:
        paginator = Paginator(postlist, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        return render(request, 'network/follow.html', {'page':page})

@login_required(login_url='login')
def editprofile(request):
    user = User.objects.get(username=request.user.username)
    if (request.method == "POST"):
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        image = request.POST["image"]
        user.first_name = first_name
        user.last_name = last_name
        user.image = image
        user.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request,"network/editprofile.html")


def showfollowers(request):
    follower = Profile.objects.filter(target=request.user)
    # paginator = Paginator(follower, 10)
    # page_number = request.GET.get('page')
    # page = paginator.get_page(page_number)
    if not follower:
        message = "Its Lonely here... Lets start by gaining followers!"
        token = False
    else:
        message = "Looks like a great circle!"
        token = True
    # token = True
    # message = "Hey There"
    return render(request,"network/showfollowers.html",{
        # "page": page,
        'followers': follower,
        'msg': message,
        'token' : token,
    })
def showfollowing(request):
    following = Profile.objects.filter(follower=request.user)
    # paginator = Paginator(follower, 10)
    # page_number = request.GET.get('page')
    # page = paginator.get_page(page_number)
    if not following:
        message = "Its Lonely here... Lets start by following someone!"
        token = False
    else:
        message = "Looks like a great circle!"
        token = True
    return render(request,"network/showfollowing.html",{
        # "page": page,
        'followers': following,
        'msg': message,
        'token' : token
    })