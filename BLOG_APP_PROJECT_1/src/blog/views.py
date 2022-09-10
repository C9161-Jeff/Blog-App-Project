import imp
from multiprocessing import context
import re
from django.shortcuts import render, redirect
from .models import Post, Like
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404

def post_list(request):
    qs = Post.objects.filter(status='p')
    context = {
        'object_list' : qs
    }
    return render (request, "blog/post_list.html", context )

def post_create(request):
    # form = PostForm(request.POST or None, request.FILES or None)
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # print(request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # messages.success(request, "Post created successfully!")
            return redirect("blog:list")
    context = { 
        'form' : form
    }
    return render (request, "blog/post_create.html", context)

def post_detail(request, slug):
    print(request.user)
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = obj
            comment.save()
            return redirect("blog:detail", slug=slug)
            # return redirect(request.path)
    context = {
        "object" : obj,
        "form" : form
    }
    
    return render(request, "blog/post_detail.html", context)
   
def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
#     if request.user.id != obj.author.id:
#         # return HttpResponse("You are not authorized!")
#         messages.warning(request, "You are not a writer of this post !")
#         return redirect("blog:list")
    if form.is_valid():
        form.save()
#         messages.success(request, "Post updated !!")
        return redirect("blog:list")
    context = {
        "object" : obj,
        "form" : form
    }
    return render(request, "blog/post_update.html", context)

# @login_required()
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    # if request.user.id != obj.author.id:
#         # return HttpResponse("You are not authorized!")
#         messages.warning(request, "You are not a writer of this post !")
#         return redirect("blog:list")
    if request.method == "POST":
        obj.delete()
#         messages.success(request, "Post deleted !!")
        return redirect("blog:list")
    
    context = {
        "object" : obj
    }
    return render(request, "blog/post_delete.html", context)

# @login_required()

def like(request, slug):
    if request.method == "POST":
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs.exists():
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect("blog:detail", slug=slug)
    
    
    # return redirect("blog:detail", slug=slug)


    # "like_qs" : like_qs,
    #     'kitap' : comment,
    #     'kim': kim
    #  comment = Comment.objects.all( )
    #  kim = request.user
    # like_qs = Like.objects.filter(user=request.user, post=obj)
    # if request.user.is_authenticated:
    #     PostView.objects.get_or_create(user=request.user, post=obj)

# @login_required()


#     #    