# members/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'members'

urlpatterns = [

    #path('', views.index, name='index'),

    ###################################################
    ###### USER AUTHENTICATION VIEWS BEGINS HERE ######
    ###################################################

    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("reset-password", views.resetPassword, name="resetPassword"),
    path("logout", views.logout, name="logout"),

    ###################################################
    #### USER AUTH PASSWORD RESET VIEWS BWGIN HERE ####
    ###################################################

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="members/reset_password.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="members/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="members/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="members/password_reset_done.html"),
         name='password_reset_complete'),

    ###############################################################
    ##### VIEW USER ACCOUNT BACKEND (LIST) VIEWS BEGINS HERE ######
    ###############################################################

    path("account", views.account, name="account"),

    ################################################################
    ##### MANAGE USER MEMBER BACKEND (CRUD) VIEWS BEGINS HERE ######
    ################################################################

    path("personal-info", views.personalInfo, name="personalInfo"),
    path("education-history", views.educationHistory, name="educationHistory"),
    path("social-profile", views.socialProfile, name="socialProfile"),
    #path("change-password", views.changePassword, name='changePassword'),

    ###########################################################
    ### LIST USERS C-ADMIN BACKEND (LIST) VIEWS BEGINS HERE ###
    ###########################################################

    path("users", views.users, name="users"),

    ###########################################################
    ## MANAGE USERS C-ADMIN BACKEND (CRUD) VIEWS BEGINS HERE ##
    ###########################################################

    path("<int:userid>/user", views.userUpdate, name="userUpdate"),
    path("user/<int:userid>/personalInfo", views.userPersonalInfo, name="userPersonalInfo"),
    path("user/<int:userid>/userEducationHistory", views.userEducationHistory, name="userEducationHistory"),
    path("user/<int:userid>/userSocialProfile", views.userSocialProfile, name="userSocialProfile"),
    path("user/<int:userid>/userSettings", views.userSettings, name="userSettings"),
    path("users/action", views.usersBulkAction, name="usersBulkAction"),
    #path("users/filter", views.usersFilter, name="usersFilter"),
    #url(r'^search/$', views.search, name='search'),

]