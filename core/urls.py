# core/urls.py

from django.urls import path
from . import views
import posts.views

app_name = 'core'

urlpatterns = [

    ###################################################
    ####### CORE FRONTEND VIEWS BEGINS HERE ###########
    ###################################################

    path('', views.index, name='index'),
    path('about', views.about, name='about'),

    ###############################################################
    #### LIST POEMS (POSTS) FRONTEND (LIST) VIEWS BEGINS HERE #####
    ###############################################################

    path("poem/<str:slug>", views.poem, name="poem"),

    ##############################################################
    #### VIEW POEM (POSTS) FRONTEND (LIST) VIEWS BEGINS HERE #####
    ##############################################################

    path("poems", views.poems, name="poems"),

    ####################################################################
    ## LIST POEM (POSTS) CATEGORY - FRONTEND (LIST) VIEWS BEGINS HERE ##
    ####################################################################

    path("poems/<str:cat_slug>/", views.poemsCategory, name="poemsCategory"),

    ########################################################################
    ## LIST POEM (POSTS) SUB CATEGORY - FRONTEND (LIST) VIEWS BEGINS HERE ##
    ########################################################################

    path("poems/<str:cat_slug>/<str:sub_cat_slug>", views.poemsSubCategory, name="poemsSubCategory"),

    ##########################################################
    ##### LIST MEMBER FRONTEND (LIST) VIEWS BEGINS HERE ######
    ##########################################################

    path("poets", views.poets, name="poets"),
    path("poets/region/<str:poet_region>", views.poetsRegion, name="poetsRegion"),
    path("poets/gender/<str:poet_gender>", views.poetsGender, name="poetsGender"),

    ##################################################################
    ##### VIEW MEMBER PROFILE FRONTEND (LIST) VIEWS BEGINS HERE ######
    ##################################################################

    path("poet/<str:username>", views.poet, name="poet"),
    path("follow/", views.follow, name="follow"),
    path("like/", views.like, name="like"),
    path("bookmark/", views.bookmark, name="bookmark"),
    path("downvote/", views.downvote, name="downvote"),
    path("upvote/", views.upvote, name="upvote"),

]