# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostCategory, PostSubCategory
from .forms import CategoryForm, SubCategoryForm, BulkActionsForm, PostForm, PostBulkActionsForm
from members.models import User, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from posts.filters import PostFilter, PostCategoryFilter, PostSubCategoryFilter

# Create your views here.

################################################################
##### LIST POSTS - MEMBER BACKEND (LIST) VIEWS BEGINS HERE #####
################################################################

@login_required
def posts(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    current_user = get_object_or_404(User, pk=request.user.id)
    post_ba_form = PostBulkActionsForm(current_user)

    user_post_object = Post.objects.filter(author=current_user).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.user.role == 'admin':
        post_list = Post.objects.all().order_by('published_date')
    elif request.user.role == 'author':
        post_list = Post.objects.filter(author=request.user).order_by('published_date')

    post_filter = PostFilter(request.GET, queryset=post_list)

    paginator = Paginator(post_filter.qs, 20)
    page = request.GET.get('page')

    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    context = {
        'all_posts': all_posts,
        'post_filter': post_filter,
        'post_ba_form': post_ba_form,
        'total_record': paginator.count,
        'user_object': user_object,
        'user_profile': user_profile,
        'total_uv': total_uv
    }

    return render(request, 'posts/posts.html', context)




'''
@login_required
def postFilter(request):

    post_ba_form = PostBulkActionsForm()
    post_filter_form = PostFilterForm()

    if request.method == 'POST':

        fl_form = PostFilterForm(request.POST)

        if fl_form.is_valid():

            cat_filter = fl_form.cleaned_data.get('filter')

            if cat_filter == '':

                messages.error(request, "Filter unsuccessful! Select at least one category filter to apply")
                return redirect('posts:posts')

            else:

                if request.user.role == 'author':

                    all_posts = Post.objects.filter(category=cat_filter, author=request.user).all()

                elif request.user.role == 'admin':

                    all_posts = Post.objects.filter(category=cat_filter).all()

                else:

                    messages.error(request, "Unable to apply category filter")
                    return redirect('posts:posts')

                context = {
                    'all_posts': all_posts,
                    'post_ba_form': post_ba_form,
                    'post_filter_form': post_filter_form
                }

                messages.success(request, "Filter applied successfully: Returned <b>"+str(all_posts.count())+"</b> result(s)")
                return render(request, 'posts/posts.html', context)

        else:

            messages.error(request, "Filter unsuccessful! Check form fields for error(s)")
            return redirect('posts:posts')

    elif request.method == 'GET':

        return redirect('posts:posts')
'''







###################################################################
##### MANAGE POSTS - MEMBER BACKEND (CRUD) VIEWS BEGINS HERE ######
###################################################################

def load_subcategory(request):
    category_id = request.GET.get('category')
    subcategory = PostSubCategory.objects.filter(category=category_id).order_by('name')
    return render(request, 'posts/subcat_dlo.html', {'subcategory': subcategory})




@login_required
def postCreate(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    user_post_object = Post.objects.filter(author=current_user).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():

            pf_state = post_form.save(commit=False)
            pf_state.author = request.user
            pf_state.save()

            messages.success(request, 'Your poem has been submitted successfully for review!')
            return redirect('posts:posts')

        else:

            context = {
                'post_form': post_form,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }

            messages.error(request, 'Unable to submit poem! - Check form fields for errors!')
            return render(request, 'posts/post_new.html', context)

    elif request.method == 'GET':

        post_form = PostForm()

        context = {
            'post_form': post_form,
            'user_object': user_object,
            'user_profile': user_profile,
            'total_uv': total_uv
        }

        return render(request, 'posts/post_new.html', context)





@login_required
def postUpdate(request, pid):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    post_obj = get_object_or_404(Post, pk=pid)
    post_update_form = PostForm(instance=post_obj)

    user_post_object = Post.objects.filter(author=current_user).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        post_update_form = PostForm(request.POST, request.FILES, instance=post_obj)

        if post_update_form.is_valid():

            post_update_form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('posts:posts')

        else:

            context = {
                'post_update_form': post_update_form,
                'pid': pid,
                'post_obj': post_obj,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }

            messages.error(request, 'Post update unsuccessful!, Check form fields for error(s)')
            return render(request, 'posts/post_edit.html', context)

    elif request.method == 'GET':

        context = {
            'post_update_form': post_update_form,
            'pid': pid,
            'post_obj': post_obj,
            'user_object': user_object,
            'user_profile': user_profile,
            'total_uv': total_uv
        }

        return render(request, 'posts/post_edit.html', context)






@login_required
def postDelete(request, pid):

    if request.method == 'POST':

        delete_post = get_object_or_404(Post, pk=pid)
        delete_post.delete()
        messages.success(request, "Post has been deleted successfully")
        return redirect('posts:posts')

    else:

        return redirect('posts:posts')


@login_required
def postBulkAction(request):

    current_user = get_object_or_404(User, pk=request.user.id)

    if request.method == 'POST':

        post_ba_form = PostBulkActionsForm(current_user, request.POST)

        if post_ba_form.is_valid():

            sel_action = post_ba_form.cleaned_data.get('action')
            sel_posts = request.POST.getlist('checked_id')

            if not sel_posts:

                messages.error(request, "Action unsuccessful! - Check at least one post to perform an action on")
                return redirect('posts:posts')

            else:

                if sel_action == 'trash':

                    action_delete = Post.objects.filter(id__in=sel_posts).delete()
                    if action_delete:

                        messages.success(request, "All selected post(s) has been deleted successfully")
                        return redirect('posts:posts')

                    else:

                        messages.error(request, "Action unsuccessful! Unable to delete all selected post(s)")
                        return redirect('posts:posts')

                elif sel_action == 'pending review' or sel_action == 'published':

                    for pid in sel_posts:

                        get_post = get_object_or_404(Post, pk=pid)
                        get_post.status = sel_action
                        get_post.save()

                    messages.success(request, "All selected post(s) status has been changed to <b>"+ sel_action +"</b>")
                    return redirect('posts:posts')

                elif sel_action == '-1':

                    messages.error(request, "Please choose an action to perform e.g Move to Trash")
                    return redirect('posts:posts')

        else:

            messages.error(request, "Bulk action unsuccessful - Check form field(s) for error")
            return redirect('posts:posts')

    else:

        return redirect('posts:posts')



###################################################################
## LIST POST CATEGORY - C-ADMIN BACKEND (LIST) VIEWS BEGINS HERE ##
###################################################################

@login_required
def category(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    user_post_object = Post.objects.filter(author=current_user).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    add_cat_form = CategoryForm()
    cat_ba_form = BulkActionsForm()

    if request.method == 'GET':

        #poet_posts = Post.objects.filter(author=request.user).all().order_by('published_date')
        category_list = PostCategory.objects.all().order_by('name')

        post_cat_filter = PostCategoryFilter(request.GET, queryset=category_list)

        paginator = Paginator(post_cat_filter.qs, 2)

        page = request.GET.get('page')

        try:
            all_category = paginator.page(page)
        except PageNotAnInteger:
            all_category = paginator.page(1)
        except EmptyPage:
            all_category = paginator.page(paginator.num_pages)

        context = {
            'add_cat_form': add_cat_form,
            'cat_ba_form': cat_ba_form,
            #'poet_posts': poet_posts,
            'all_category': all_category,
            'post_cat_filter': post_cat_filter,
            'total_record': paginator.count,
            'user_object': user_object,
            'user_profile': user_profile,
            'total_uv': total_uv
        }

        return render(request, 'posts/category.html', context)



####################################################################
## MANAGE POSTS CATEGORY C-ADMIN BACKEND (CRUD) VIEWS BEGINS HERE ##
####################################################################

def categoryCreate(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    poet_posts = Post.objects.filter(author=request.user).all()
    all_category = PostCategory.objects.all()

    if poet_posts:

        upvoters = []

        for uv in poet_posts:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        add_cat_form = CategoryForm(request.POST)

        if add_cat_form.is_valid():

            name = add_cat_form.cleaned_data.get('name')
            description = add_cat_form.cleaned_data.get('description')

            existing_category = PostCategory.objects.filter(name=name)

            if existing_category:

                context = {
                    'add_cat_form': add_cat_form,
                    'poet_posts': poet_posts,
                    'all_category': all_category,
                    'user_object': user_object,
                    'user_profile': user_profile,
                    'total_uv': total_uv
                }

                messages.error(request, 'Category name already exists. Try a different name!')
                return render(request, 'posts/category.html', context)

            else:

                new_category = PostCategory(name=name, slug=name, description=description)
                new_category.save()

                messages.success(request, 'New Category Added Successfully!')
                return redirect('posts:category')
        else:

            context = {
                'add_cat_form': add_cat_form,
                'poet_posts': poet_posts,
                'all_category': all_category,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }

            messages.error(request, 'Unable to create category! Check form fields for error(s)')
            return render(request, 'posts/category.html', context)

    elif request.method == 'GET':

        return redirect('posts:category')




def categoryUpdate(request, catid):

    add_cat_form = CategoryForm()
    cat_ba_form = BulkActionsForm()

    if request.method == 'POST':

        if request.POST.get('catName' + str(catid)) == '':
            messages.error(request, "Please enter a category name")
            return redirect('posts:category')

        else:

            cat_name = request.POST.get('catName' + str(catid))
            existing_category = PostCategory.objects.filter(name=cat_name)

            if existing_category:
                messages.error(request, 'Category name already exists. Try a different name!')
                return redirect('posts:category')

        if request.POST.get('catDesc' + str(catid)) == '':
            messages.error(request, "Please enter a category description")
            return redirect('posts:category')

        else:

            cat_desc = request.POST.get('catDesc' + str(catid))

        edit_category = PostCategory.objects.get(pk=catid)

        if edit_category is not None:

            edit_category.name = cat_name
            edit_category.slug = cat_name
            edit_category.description = cat_desc

            edit_category.save()

            messages.success(request, "Category Updated Successfully")
            return redirect('posts:category')

        else:

            messages.error(request, "Category Update Unsuccessful! - Check form fields for error")
            return redirect('posts:category')

    elif request.method == 'GET':

        return redirect('posts:category')




def categoryDelete(request, catid):

    if request.method == 'GET':

        delete_category = PostCategory.objects.get(pk=catid)
        delete_category.delete()
        messages.success(request, "Category has been deleted successfully")
        return redirect('posts:category')

    else:

        return redirect('posts:category')



def categoryBulkAction(request):

    if request.method == 'POST':

        cat_ba_form = BulkActionsForm(request.POST)

        if cat_ba_form.is_valid():

            sel_action = cat_ba_form.cleaned_data.get('action')
            sel_cats = request.POST.getlist('checked_id')

            if not sel_cats:

                messages.error(request, "Action Unsuccessful! - Check at least one category to delete")
                return redirect('posts:category')

            else:

                if sel_action == 'trash':

                    PostCategory.objects.filter(id__in=sel_cats).delete()
                    messages.success(request, "All selected category(s) has been deleted successfully")
                    return redirect('posts:category')

                elif sel_action == '-1':

                    messages.error(request, "Please choose an action to perform e.g Move to Trash")
                    return redirect('posts:category')

        else:

            messages.error(request, "Bulk action unsuccessful - Check form fields for error")
            return render(request, 'posts/category.html', {'cat_ba_form': cat_ba_form})

    else:

        return redirect('posts:category')



#######################################################################
## LIST POST SUB CATEGORY - C-ADMIN BACKEND (LIST) VIEWS BEGINS HERE ##
#######################################################################

def subCategory(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    user_post_object = Post.objects.filter(author=current_user).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    add_sub_cat_form = SubCategoryForm()
    sub_cat_ba_form = BulkActionsForm()
    all_parent_category = PostCategory.objects.all()

    if request.method == 'GET':

        #poet_posts = Post.objects.filter(author=request.user).all()
        sub_category_list = PostSubCategory.objects.all().order_by('name')
        post_sub_cat_filter = PostSubCategoryFilter(request.GET, queryset=sub_category_list)

        paginator = Paginator(post_sub_cat_filter.qs, 2)

        page = request.GET.get('page')

        try:
            all_sub_category = paginator.page(page)
        except PageNotAnInteger:
            all_sub_category = paginator.page(1)
        except EmptyPage:
            all_sub_category = paginator.page(paginator.num_pages)

        context = {
            'add_sub_cat_form': add_sub_cat_form,
            'sub_cat_ba_form': sub_cat_ba_form,
            #'poet_posts': poet_posts,
            'post_sub_cat_filter': post_sub_cat_filter,
            'all_sub_category': all_sub_category,
            'all_parent_category': all_parent_category,
            'total_record': paginator.count,
            'user_object': user_object,
            'user_profile': user_profile,
            'total_uv': total_uv
        }

        return render(request, 'posts/sub_category.html', context)




########################################################################
## MANAGE POSTS SUB CATEGORY C-ADMIN BACKEND (CRUD) VIEWS BEGINS HERE ##
########################################################################

def subCategoryCreate(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    poet_posts = Post.objects.filter(author=request.user).all()
    all_sub_category = PostSubCategory.objects.all()

    if poet_posts:

        upvoters = []

        for uv in poet_posts:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        add_sub_cat_form = SubCategoryForm(request.POST)

        if add_sub_cat_form.is_valid():

            cat_id = add_sub_cat_form.cleaned_data.get('category')
            name = add_sub_cat_form.cleaned_data.get('name')
            description = add_sub_cat_form.cleaned_data.get('description')

            existing_sub_category = PostSubCategory.objects.filter(name=name)

            if existing_sub_category:

                context = {
                    'add_sub_cat_form': add_sub_cat_form,
                    'poet_posts': poet_posts,
                    'all_sub_category': all_sub_category,
                    'user_object': user_object,
                    'user_profile': user_profile,
                    'total_uv': total_uv
                }

                messages.error(request, 'Sub category name already exists. Try a different name!')
                return render(request, 'posts/sub-category.html', context)

            else:

                new_sub_category = PostSubCategory(category=cat_id, name=name, slug=name, description=description)
                new_sub_category.save()

                messages.success(request, 'New Sub Category Added Successfully!')
                return redirect('posts:subCategory')
        else:

            context = {
                'add_sub_cat_form': add_sub_cat_form,
                'poet_posts': poet_posts,
                'all_sub_category': all_sub_category,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }

            messages.error(request, 'Unable to create sub category! Check form fields for error(s)')
            return render(request, 'posts/sub-category.html', context)

    elif request.method == 'GET':

        return redirect('posts:subCategory')





def subCategoryUpdate(request, subcatid):

    if request.method == 'POST':

        if request.POST.get('subCatParent' + str(subcatid)) == '':
            messages.error(request, "Please select a parent category")
            return redirect('posts:subCategory')
        else:
            sub_cat_parent = request.POST.get('subCatParent' + str(subcatid))

        if request.POST.get('subCatName' + str(subcatid)) == '':
            messages.error(request, "Please enter a category name")
            return redirect('posts:subCategory')
        else:
            sub_cat_name = request.POST.get('subCatName' + str(subcatid))

            #existing_sub_category = PostSubCategory.objects.filter(name=sub_cat_name)
            #if existing_sub_category:
            #    messages.error(request, 'Sub category name already exists. Try a different name!')
            #    return redirect('posts:subCategory')

        if request.POST.get('subCatDesc' + str(subcatid)) == '':
            messages.error(request, "Please enter a sub category description")
            return redirect('posts:subCategory')
        else:
            sub_cat_desc = request.POST.get('subCatDesc' + str(subcatid))

        edit_sub_category = PostSubCategory.objects.get(pk=subcatid)

        if edit_sub_category is not None:

            edit_sub_category.category = PostCategory.objects.get(pk=sub_cat_parent)
            edit_sub_category.name = sub_cat_name
            edit_sub_category.slug = sub_cat_name
            edit_sub_category.description = sub_cat_desc

            edit_sub_category.save()

            messages.success(request, "Sub category has been updated successfully")
            return redirect('posts:subCategory')

        else:

            messages.error(request, "Internal error: Unable to update sub category!")
            return redirect('posts:subCategory')

    elif request.method == 'GET':

        return redirect('posts:subCategory')





def subCategoryDelete(request, subcatid):

    if request.method == 'GET':

        delete_sub_category = PostSubCategory.objects.get(pk=subcatid)
        delete_sub_category.delete()
        messages.success(request, "Sub category has been deleted successfully")
        return redirect('posts:subCategory')

    else:

        return redirect('posts:subCategory')





def subCategoryBulkAction(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=user_object)

    all_parent_category = PostCategory.objects.all()

    if request.method == 'POST':

        sub_cat_ba_form = BulkActionsForm(request.POST)

        if sub_cat_ba_form.is_valid():

            sel_action = sub_cat_ba_form.cleaned_data.get('action')
            sel_sub_cats = request.POST.getlist('checked_id')

            if sel_action == 'trash':

                if not sel_sub_cats:

                    messages.error(request, "Action Unsuccessful! - Check at least one sub category to delete")
                    return redirect('posts:subCategory')

                else:

                    PostSubCategory.objects.filter(id__in=sel_sub_cats).delete()
                    messages.success(request, "All selected sub category(s) has been deleted successfully")
                    return redirect('posts:subCategory')

            elif sel_action == '-1':

                messages.error(request, "Please choose an action to perform e.g Move to Trash")
                return redirect('posts:subCategory')

        else:

            context = {
                'all_parent_category': all_parent_category,
                'sub_cat_ba_form': sub_cat_ba_form,
                'user_object': user_object,
                'user_profile': user_profile
            }

            messages.error(request, "Bulk action unsuccessful - Check form fields for error")
            return render(request, 'posts/sub-category.html', context)

    else:

        return redirect('posts:subCategory')
