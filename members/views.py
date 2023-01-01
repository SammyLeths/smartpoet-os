# members/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, views as auth_views, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Profile
from posts.models import Post
from .forms import LoginForm, RegisterForm, PersonalInfoForm, EducationHistoryForm, SocialProfilesForm, BulkActionsForm, UserSettingsForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from members.filters import UserFilter

#from allauth.account.forms import ChangePasswordForm

# Create your views here.

###################################################
###### USER AUTHENTICATION VIEWS BEGINS HERE ######
###################################################

def register(request):
    
    if request.method == 'POST':

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():

            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')
            firstname = register_form.cleaned_data.get('first_name')
            lastname = register_form.cleaned_data.get('last_name')

            # Ensure password matches confirmation
            password = register_form.cleaned_data.get('password')
            confirmation = register_form.cleaned_data.get('pass_confirm')

            if password != confirmation:
                messages.error(request, 'Passwords must match.!')
                return render(request, 'members/register.html', {'reg_form': register_form})

            # Ensure email dosen't already exists
            existing_email = User.objects.filter(email=email).all()

            if existing_email:
                messages.error(request, 'Your email has already been registered by another user!')
                return render(request, 'members/register.html', {'reg_form': register_form})

            # Attempt to create new user
            try:

                user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
                user.save()

                profile = Profile()
                profile.user = user
                profile.save()

                messages.success(request, 'Registration Successful! Login to your account')
                return redirect('members:login')

            except IntegrityError:

                messages.error(request, 'Username already taken')
                return render(request, 'members/register.html', {'reg_form': register_form})

        else:

            messages.error(request, 'Registration unsuccessful! Check form fields for error(s)')
            return render(request, 'members/register.html', {'reg_form': register_form})

    else:

        register_form = RegisterForm()
        context = {
            'reg_form': register_form
        }

        return render(request, 'members/register.html', context)





def login(request):

    if request.method == 'POST':

        login_form = LoginForm(request.POST)

        if login_form.is_valid():

            # Attempt to sign user in
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user_object = User.objects.filter(username=username).first()

            if user_object is None:

                messages.error(request, 'User does not exists!')
                return render(request, 'members/login.html', {'login_form': login_form})

            elif (not user_object.is_active):

                messages.error(request, 'Your account has been disabled. Contact support')
                return render(request, 'members/login.html', {'login_form': login_form})

            else:

                user = authenticate(request, username=username, password=password)

                # Check if authentication is successful
                if user is not None:

                    auth_login(request, user)
                    messages.success(request, 'You have logged in successfully')
                    return redirect('members:account')

                else:

                    messages.error(request, 'Invalid username and/or password.')
                    return render(request, 'members/login.html', {'login_form': login_form})
        else:

            messages.error(request, 'Login unsuccessful! Check form fields for error(s)')
            return render(request, 'members/login.html', {'login_form': login_form})
    else:

        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'members/login.html', context)




@login_required
def resetPassword(request):

    return render(request, 'members/login.html')





@login_required
def logout(request):

    auth_logout(request)
    return redirect('members:login')





###############################################################
##### VIEW USER ACCOUNT BACKEND (LIST) VIEWS BEGINS HERE ######
###############################################################

@login_required
def account(request):

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

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)

    context = {
        'pi_form': pi_form,
        'eh_form': eh_form,
        'sp_form': sp_form,
        'user_object': user_object,
        'user_profile': user_profile,
        'user_post_object': user_post_object,
        'total_uv': total_uv
    }

    return render(request, 'members/account.html', context)




################################################################
##### MANAGE USER MEMBER BACKEND (CRUD) VIEWS BEGINS HERE ######
################################################################

@login_required
def personalInfo(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    #cp_form = ChangePasswordForm(user_object)

    if request.method == 'POST':

        pi_form = PersonalInfoForm(request.POST, request.FILES, instance=user_object)

        if pi_form.is_valid():
            pi_form.save()
            user_object.status = 'profile activated'
            user_object.save()
            messages.success(request, 'Personal Info Updated Successfully!')
            return redirect('members:account')
        else:
            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                #'cp_form': cp_form,
            }
            messages.error(request, 'Personal Info Update Unsuccessful!, Check form fields for error(s)')
            return render(request, 'members/account.html', context)

    elif request.method == 'GET':

        return redirect('members:account')




@login_required
def educationHistory(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    #cp_form = ChangePasswordForm(user_object)

    if request.method == 'POST':
        eh_form = EducationHistoryForm(request.POST, instance=user_object)

        if eh_form.is_valid():
            eh_form.save()
            messages.success(request, 'Education History Updated Successfully!')
            return redirect('members:account')
        else:
            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                #'cp_form': cp_form
            }
            messages.error(request, 'Education History Update Unsuccessful!, Check form fields for error(s)')
            return render(request, 'members/account.html', context)

    elif request.method == 'GET':

        return redirect('members:account')




@login_required
def socialProfile(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    #cp_form = ChangePasswordForm(user_object)

    if request.method == 'POST':

        sp_form = SocialProfilesForm(request.POST, instance=user_object)

        if sp_form.is_valid():
            sp_form.save()
            messages.success(request, 'Social Profiles Updated Successfully!')
            return redirect('members:account')
        else:
            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                #'cp_form': cp_form
            }
            messages.error(request, 'Social Profiles Update Unsuccessful! Check form fields for error(s)')
            return render(request, 'members/account.html', context)

    elif request.method == 'GET':

        return redirect('members:account')



'''
@login_required
def changePassword(request):

    current_user = request.user
    user_object = User.objects.get(pk=current_user.id)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    cp_form = ChangePasswordForm(user_object)

    if request.method == 'POST':

        cp_form = ChangePasswordForm(user_object, request.POST)

        if cp_form.is_valid():

            user = cp_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('members:account')

        else:

            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                'cp_form': cp_form
            }

            messages.error(request, 'Password update unsuccessful! Check form fields for error(s)')
            return render(request, 'members/account.html', context)

    else:

        return redirect('members:account')

'''





###########################################################
### LIST USERS C-ADMIN BACKEND (LIST) VIEWS BEGINS HERE ###
###########################################################

@login_required
def users(request):

    if request.method == 'GET':

        current_user = request.user
        user_object = User.objects.get(pk=current_user.id)
        user_profile = Profile.objects.get(user=user_object)

        user_ba_form = BulkActionsForm()

        user_list = User.objects.annotate(total_posts=Count('user')).order_by('date_joined')
        user_filter = UserFilter(request.GET, queryset=user_list)

        user_post_object = Post.objects.filter(author=current_user).order_by('published_date').all()

        if user_post_object:

            upvoters = []

            for uv in user_post_object:
                upvoters.append(uv.upvotes.count())
                total_uv = sum(upvoters)
        else:

            total_uv = 0

        paginator = Paginator(user_filter.qs, 20)
        page = request.GET.get('page')

        try:
            all_users = paginator.page(page)
        except PageNotAnInteger:
            all_users = paginator.page(1)
        except EmptyPage:
            all_users = paginator.page(paginator.num_pages)

        context = {
            'all_users': all_users,
            'user_ba_form': user_ba_form,
            'user_filter': user_filter,
            'total_record': paginator.count,
            'user_object': user_object,
            'user_profile': user_profile,
            'total_uv': total_uv
        }

        return render(request, 'members/users.html', context)





###########################################################
## MANAGE USERS C-ADMIN BACKEND (CRUD) VIEWS BEGINS HERE ##
###########################################################

@login_required
def userUpdate(request, userid):

    user_object = User.objects.get(pk=userid)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    us_form = UserSettingsForm(instance=user_object)

    current_user = request.user
    logged_user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=logged_user_object)

    user_post_object = Post.objects.filter(author=logged_user_object).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    context = {
        'pi_form': pi_form,
        'eh_form': eh_form,
        'sp_form': sp_form,
        'us_form': us_form,
        'user_object': user_object,
        'user_profile': user_profile,
        'total_uv': total_uv
    }

    return render(request, 'members/user_edit.html', context)


@login_required
def userPersonalInfo(request, userid):

    user_object = get_object_or_404(User, pk=userid)
    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    us_form = UserSettingsForm(instance=user_object)

    current_user = request.user
    logged_user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=logged_user_object)

    user_post_object = Post.objects.filter(author=logged_user_object).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        pi_form = PersonalInfoForm(request.POST, request.FILES, instance=user_object)

        if pi_form.is_valid():
            pi_form.save()
            messages.success(request, user_object.username.capitalize()+"'s Personal Info Updated Successfully!")
            return redirect('members:userUpdate', userid)

        else:

            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                'us_form': us_form,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }
            messages.error(request, user_object.username.capitalize()+"'s Personal Info Update Unsuccessful!, Check form fields for error(s)")
            return render(request, 'members/user_edit.html', context)

    elif request.method == 'GET':

        return redirect('members:userUpdate', userid)


@login_required
def userEducationHistory(request, userid):

    user_object = get_object_or_404(User, pk=userid)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    us_form = UserSettingsForm(instance=user_object)

    current_user = request.user
    logged_user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=logged_user_object)

    user_post_object = Post.objects.filter(author=logged_user_object).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        eh_form = EducationHistoryForm(request.POST, instance=user_object)

        if eh_form.is_valid():
            eh_form.save()
            messages.success(request, user_object.username.capitalize() + "'s Education History Updated Successfully!")
            return redirect('members:userUpdate', userid)

        else:

            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                'us_form': us_form,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }
            messages.error(request,
                           user_object.username.capitalize() + "'s Education History Update Unsuccessful!, Check form fields for error(s)")
            return render(request, 'members/user_edit.html', context)

    elif request.method == 'GET':

        return redirect('members:userUpdate', userid)


@login_required
def userSocialProfile(request, userid):

    user_object = get_object_or_404(User, pk=userid)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    us_form = UserSettingsForm(instance=user_object)

    current_user = request.user
    logged_user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=logged_user_object)

    user_post_object = Post.objects.filter(author=logged_user_object).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        sp_form = SocialProfilesForm(request.POST, instance=user_object)

        if sp_form.is_valid():
            sp_form.save()
            messages.success(request, user_object.username.capitalize() + "'s Social Profile Updated Successfully!")
            return redirect('members:userUpdate', userid)

        else:

            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                'us_form': us_form,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }
            messages.error(request, user_object.username.capitalize() + "'s Social Profile Update Unsuccessful!, Check form fields for error(s)")
            return render(request, 'members/user_edit.html', context)

    elif request.method == 'GET':

        return redirect('members:userUpdate', userid)


@login_required
def userSettings(request, userid):

    user_object = get_object_or_404(User, pk=userid)

    pi_form = PersonalInfoForm(instance=user_object)
    eh_form = EducationHistoryForm(instance=user_object)
    sp_form = SocialProfilesForm(instance=user_object)
    us_form = UserSettingsForm(instance=user_object)

    current_user = request.user
    logged_user_object = User.objects.get(pk=current_user.id)
    user_profile = Profile.objects.get(user=logged_user_object)

    user_post_object = Post.objects.filter(author=logged_user_object).order_by('published_date').all()

    if user_post_object:

        upvoters = []

        for uv in user_post_object:
            upvoters.append(uv.upvotes.count())
            total_uv = sum(upvoters)
    else:

        total_uv = 0

    if request.method == 'POST':

        us_form = UserSettingsForm(request.POST, instance=user_object)

        if us_form.is_valid():
            us_form.save()
            messages.success(request, user_object.username.capitalize() + "'s User Settings Updated Successfully!")
            return redirect('members:userUpdate', userid)

        else:

            context = {
                'pi_form': pi_form,
                'eh_form': eh_form,
                'sp_form': sp_form,
                'us_form': us_form,
                'user_object': user_object,
                'user_profile': user_profile,
                'total_uv': total_uv
            }
            messages.error(request, user_object.username.capitalize() + "'s User Settings Update Unsuccessful! Check form fields for error(s)")
            return render(request, 'members/user_edit.html', context)

    elif request.method == 'GET':

        return redirect('members:userUpdate', userid)



@login_required
def usersBulkAction(request):

    if request.method == 'POST':

        user_ba_form = BulkActionsForm(request.POST)

        if user_ba_form.is_valid():

            sel_action = user_ba_form.cleaned_data.get('action')
            sel_users = request.POST.getlist('checked_id')

            if not sel_users:

                messages.error(request, "Action unsuccessful! - Check at least one user to perform an action on")
                return redirect('members:users')

            else:

                if sel_action == 'trash':

                    action_delete = User.objects.filter(id__in=sel_users).delete()
                    if action_delete:
                        messages.success(request, "All selected user(s) has been deleted successfully")
                        return redirect('members:users')
                    else:
                        messages.error(request, "Action unsuccessful! Unable to delete all selected user(s)")
                        return redirect('members:users')

                elif sel_action == 'pending email verification' or sel_action == 'email verified' or sel_action == 'pending profile activation' or sel_action == 'profile activated':

                    for uid in sel_users:

                        get_user = get_object_or_404(User, pk=uid)
                        get_user.status = sel_action
                        get_user.save()

                    messages.success(request, "All selected user(s) profile status have been changed to <b>"+ sel_action +"</b>")
                    return redirect('members:users')

                elif sel_action == 'admin' or sel_action == 'author':

                    for uid in sel_users:

                        get_user = get_object_or_404(User, pk=uid)
                        get_user.role = sel_action
                        get_user.save()

                    messages.success(request, "All selected user(s) role have been changed to <b>"+ sel_action +"</b>")
                    return redirect('members:users')

                elif sel_action == '0' or sel_action == '1':

                    for uid in sel_users:

                        get_user = get_object_or_404(User, pk=uid)
                        get_user.is_active = sel_action
                        get_user.save()

                    messages.success(request, "All selected user(s) status have been changed to <b>"+ sel_action +"</b>")
                    return redirect('members:users')

                elif sel_action == '-1':

                    messages.error(request, "Please choose an action to perform e.g Move to Trash")
                    return redirect('members:users')

        else:

            messages.error(request, "Bulk action unsuccessful - Check form field(s) for error")
            return redirect('members:users')

    else:

        return redirect('members:users')


# CUSTOM USER FILTER VIEW

'''
def usersFilter(request):

    user_ba_form = BulkActionsForm()
    user_filter_form = UserFilterForm()

    if request.method == 'POST':

        fl_form = UserFilterForm(request.POST)

        if fl_form.is_valid():

            status_filter = fl_form.cleaned_data.get('filter')

            if status_filter == '':

                messages.error(request, "Filter unsuccessful! Select at least one status filter to apply")
                return redirect('members:users')

            else:

                object_list = User.objects.filter(status=status_filter).annotate(total_posts=Count('author')).all()

                #object_list = User.objects.annotate(total_posts=Count('author'))

                paginator = Paginator(object_list, 1)

                page = request.GET.get('page')

                try:
                    all_users = paginator.page(page)
                except PageNotAnInteger:
                    all_users = paginator.page(1)
                except EmptyPage:
                    all_users = paginator.page(paginator.num_pages)

                context = {
                    'all_users': all_users,
                    'user_ba_form': user_ba_form,
                    'user_filter_form': user_filter_form
                }

                messages.success(request, "Filter applied successfully: Returned <b>" + str(
                    paginator.count) + "</b> user(s) with <b>"+ status_filter +"</b> status")
                return render(request, 'members/users.html', context)

        else:

            messages.error(request, "Filter unsuccessful! Check form fields for error(s)")
            return redirect('members:users')

    elif request.method == 'GET':

        return redirect('members:users')
'''



'''
def search(request):

    if request.method == 'GET':

        user_list = User.objects.all()
        user_filter = UserFilter(request.GET, queryset=user_list)
        return render(request, 'members/users.html', {'filter': user_filter})
'''