# core/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from posts.models import Post, PostCategory, PostSubCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from members.models import User, Profile
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

###################################################
####### CORE FRONTEND VIEWS BEGINS HERE ###########
###################################################

def index(request):

    all_posts = Post.objects.filter(status='published').order_by('published_date')[:20]

    #all_posts = Post.objects.all().order_by('published_date')

    context = {
        'all_posts': all_posts
    }

    return render(request, 'core/index.html', context)


def about(request):

    return render(request, 'core/about.html')



###################################################
#### POEMS (POSTS) FRONTEND VIEWS BEGINS HERE #####
###################################################

def poem(request, slug):

    parent_categories = PostCategory.objects.all().order_by('name')

    poem = Post.objects.filter(slug=slug).first()

    context = {
        'poem': poem,
        'parent_categories': parent_categories,
        'poemsinglepage': 'poemsinglepage',
    }

    return render(request, 'core/poem.html', context)


def poems(request):

    parent_categories = PostCategory.objects.all().order_by('name')

    all_posts = Post.objects.filter(status='published').order_by('published_date')

    paginator = Paginator(all_posts, 20)
    page = request.GET.get('page')

    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    context = {
        'all_posts': all_posts,
        'parent_categories': parent_categories,
        'cat_slug': '',
        'cat_name': '',
        'cat_desc': '',
        'sub_cat_slug': '',
        'sub_cat_name': '',
        'sub_cat_description': '',
    }

    return render(request, 'core/poems.html', context)



def poemsCategory(request, cat_slug):

    parent_categories = PostCategory.objects.all().order_by('name')

    sel_cat = PostCategory.objects.filter(slug=cat_slug).first()

    cat_id = sel_cat.id
    cat_name = sel_cat.name
    cat_desc = sel_cat.description

    all_posts = Post.objects.filter(category=cat_id, status='published').order_by('published_date')

    paginator = Paginator(all_posts, 2)
    page = request.GET.get('page')

    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    context = {
        'all_posts': all_posts,
        'parent_categories': parent_categories,
        'cat_slug': cat_slug,
        'cat_name': cat_name,
        'cat_desc': cat_desc,
        'sub_cat_slug': '',
        'sub_cat_name': '',
        'sub_cat_desc': '',
    }

    return render(request, 'core/poems.html', context)



def poemsSubCategory(request, cat_slug, sub_cat_slug):

    parent_categories = PostCategory.objects.all().order_by('name')

    sel_sub_cat = PostSubCategory.objects.filter(slug=sub_cat_slug).first()

    sub_cat_id = sel_sub_cat.id
    sub_cat_name = sel_sub_cat.name
    sub_cat_desc = sel_sub_cat.description
    cat_name = sel_sub_cat.category.name

    all_posts = Post.objects.filter(sub_category=sub_cat_id, status='published').order_by('published_date')

    paginator = Paginator(all_posts, 2)
    page = request.GET.get('page')

    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    context = {
        'all_posts': all_posts,
        'parent_categories': parent_categories,
        'cat_slug': cat_slug,
        'cat_name': cat_name,
        'cat_desc': '',
        'sub_cat_slug': sub_cat_slug,
        'sub_cat_name': sub_cat_name,
        'sub_cat_desc': sub_cat_desc,
    }

    return render(request, 'core/poems.html', context)



###################################################
##### POETS (USER) FRONTEND VIEWS BEGINS HERE #####
###################################################


def poet(request, username):

    try:
        poet = User.objects.get(username=username)
        user_being_viewed_profile = Profile.objects.get(user=poet)
    except:
        return redirect('core:error_404')

    if request.user.is_authenticated:
        logged_in_user_profile = Profile.objects.get(user=request.user)
    else:
        logged_in_user_profile = None

    similar_poets = User.objects.filter(region=poet.region, role='author').order_by('username')[:20]

    get_poet_posts = Post.objects.filter(author=poet.id).order_by('published_date').all()

    if get_poet_posts:

        upvoters = []

        for uv in get_poet_posts:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    paginator = Paginator(get_poet_posts, 20)
    page = request.GET.get('page')

    try:
        poet_posts = paginator.page(page)
    except PageNotAnInteger:
        poet_posts = paginator.page(1)
    except EmptyPage:
        poet_posts = paginator.page(paginator.num_pages)

    context = {
        'poet': poet,
        'poet_posts': poet_posts,
        'similar_poets': similar_poets,
        'username': username,
        'user_being_viewed_profile': user_being_viewed_profile,
        'logged_in_user_profile': logged_in_user_profile,
        'total_uv': total_uv
    }

    return render(request, 'core/profile.html', context)


@login_required
@csrf_exempt
def follow(request):

    if request.method == "POST":
        user = request.POST.get('user')
        action = request.POST.get('action')

        if action == 'Follow':
            try:
                # add user whose profile is being viewed to currently logged in user's following list
                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.add(user)
                profile.save()

                # add currently logged in user to user whose profile isi being viewwed follower list
                profile = Profile.objects.get(user=user)
                profile.follower.add(request.user)
                profile.save()
                return JsonResponse({'status': 201, 'action': "Unfollow", "follower_count": profile.follower.count()},
                                    status=201)
            except:
                return JsonResponse({}, status=404)
        else:
            try:
                # add user to current user's following list
                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.remove(user)
                profile.save()

                # add current user to  user's follower list
                profile = Profile.objects.get(user=user)
                profile.follower.remove(request.user)
                profile.save()
                return JsonResponse({'status': 201, 'action': "Follow", "follower_count": profile.follower.count()},
                                    status=201)
            except:
                return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)




@csrf_exempt
def like(request):

    if request.method == "POST":
        if(not request.user.is_authenticated):
            return JsonResponse({'logged': False})
        else:
            post_id = request.POST.get('id')
            is_liked = request.POST.get('is_liked')
            try:
                post = Post.objects.get(id=post_id)
                if is_liked == 'no':
                    post.likes.add(request.user)
                    is_liked = 'yes'
                elif is_liked == 'yes':
                    post.likes.remove(request.user)
                    is_liked = 'no'
                post.save()

                return JsonResponse({'like_count': post.likes.count(), 'is_liked': is_liked, "status": 201,})
            except:
                return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)



@csrf_exempt
def bookmark(request):

    if request.method == "POST":
        if(not request.user.is_authenticated):
            return JsonResponse({'logged': False})
        else:
            post_id = request.POST.get('id')
            is_bookmarked = request.POST.get('is_bookmarked')
            try:
                post = Post.objects.get(id=post_id)
                if is_bookmarked == 'no':
                    post.bookmarks.add(request.user)
                    is_bookmarked = 'yes'
                elif is_bookmarked == 'yes':
                    post.bookmarks.remove(request.user)
                    is_bookmarked = 'no'
                post.save()

                return JsonResponse({'bookmark_count': post.bookmarks.count(), 'is_bookmarked': is_bookmarked, "status": 201,})
            except:
                return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)




@csrf_exempt
def downvote(request):

    if request.method == "POST":
        if(not request.user.is_authenticated):
            return JsonResponse({'logged': False})
        else:
            post_id = request.POST.get('id')
            is_downvoted = request.POST.get('is_downvoted')
            try:
                post = Post.objects.get(id=post_id)
                if is_downvoted == 'no':
                    post.downvotes.add(request.user)
                    is_downvoted = 'yes'
                elif is_downvoted == 'yes':
                    post.downvotes.remove(request.user)
                    is_downvoted = 'no'
                post.save()

                return JsonResponse({'downvote_count': post.downvotes.count(), 'is_downvoted': is_downvoted, "status": 201,})
            except:
                return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)




@csrf_exempt
def upvote(request):

    if request.method == "POST":
        if(not request.user.is_authenticated):
            return JsonResponse({'logged': False})
        else:
            post_id = request.POST.get('id')
            is_upvoted = request.POST.get('is_upvoted')
            try:
                post = Post.objects.get(id=post_id)
                if is_upvoted == 'no':
                    post.upvotes.add(request.user)
                    is_upvoted = 'yes'
                elif is_upvoted == 'yes':
                    post.upvotes.remove(request.user)
                    is_upvoted = 'no'
                post.save()

                return JsonResponse({'upvote_count': post.upvotes.count(), 'is_upvoted': is_upvoted, "status": 201,})
            except:
                return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)




def poets(request):

    all_poets = User.objects.filter(role='author', status='profile activated', is_active=1).annotate(total_posts=Count('user')).order_by('date_joined').all()

    paginator = Paginator(all_poets, 20)
    page = request.GET.get('page')

    try:
        all_poets = paginator.page(page)
    except PageNotAnInteger:
        all_poets = paginator.page(1)
    except EmptyPage:
        all_poets = paginator.page(paginator.num_pages)

    context = {
        'all_poets': all_poets,
        'poet_region': '',
        'poet_gender': ''
    }

    return render(request, 'core/poets.html', context)


def poetsRegion(request, poet_region):

    all_poets = User.objects.filter(role='author', status='profile activated', is_active=1, region=poet_region).annotate(total_posts=Count('user')).order_by('date_joined').all()

    # user_list = User.objects.annotate(total_posts=Count('user')).order_by('date_joined')

    paginator = Paginator(all_poets, 20)
    page = request.GET.get('page')

    try:
        all_poets = paginator.page(page)
    except PageNotAnInteger:
        all_poets = paginator.page(1)
    except EmptyPage:
        all_poets = paginator.page(paginator.num_pages)

    context = {
        'all_poets': all_poets,
        'poet_region': poet_region,
        'poet_gender': ''
    }

    return render(request, 'core/poets.html', context)



def poetsGender(request, poet_gender):

    all_poets = User.objects.filter(role='author', status='profile activated', is_active=1, gender=poet_gender).annotate(total_posts=Count('user')).order_by('date_joined').all()

    # user_list = User.objects.annotate(total_posts=Count('user')).order_by('date_joined')

    paginator = Paginator(all_poets, 20)
    page = request.GET.get('page')

    try:
        all_poets = paginator.page(page)
    except PageNotAnInteger:
        all_poets = paginator.page(1)
    except EmptyPage:
        all_poets = paginator.page(paginator.num_pages)

    context = {
        'all_poets': all_poets,
        'poet_gender': poet_gender,
        'poet_region': ''
    }

    return render(request, 'core/poets.html', context)



###################################################
##### PERMISSION/ERROR/PAGE NOT FOUND HANDLER #####
###################################################


def error_404(request, exception):
    return render(request, "core/404.html", status=404)



#def error_500(request):
#   return render(request, "core/500.html", status=500)