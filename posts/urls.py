# posts/urls.py

from django.urls import path
from . import views

# Create your urls here.

app_name = 'posts'

urlpatterns = [

    ################################################################
    ##### LIST POSTS - MEMBER BACKEND (LIST) VIEWS BEGINS HERE #####
    ################################################################

    path("all-posts", views.posts, name="posts"),
    #path("posts/filter", views.postFilter, name="postFilter"),

    ###################################################################
    ##### MANAGE POSTS - MEMBER BACKEND (CRUD) VIEWS BEGINS HERE ######
    ###################################################################

    path("ajax/load-sub-category", views.load_subcategory, name="load_subcategory"),
    path("create-poem", views.postCreate, name="postCreate"),
    path("<int:pid>/post-update", views.postUpdate, name="postUpdate"),
    path("<int:pid>/post-delete", views.postDelete, name="postDelete"),
    path("posts/action", views.postBulkAction, name="postBulkAction"),

    ###################################################################
    ## LIST POST CATEGORY - C-ADMIN BACKEND (LIST) VIEWS BEGINS HERE ##
    ###################################################################

    path("category", views.category, name="category"),

    ####################################################################
    ## MANAGE POSTS CATEGORY C-ADMIN BACKEND (CRUD) VIEWS BEGINS HERE ##
    ####################################################################

    path("category/create", views.categoryCreate, name="categoryCreate"),
    path("category/<int:catid>/update", views.categoryUpdate, name="categoryUpdate"),
    path("category/<int:catid>/delete", views.categoryDelete, name="categoryDelete"),
    path("category/action", views.categoryBulkAction, name="categoryBulkAction"),

    #######################################################################
    ## LIST POST SUB CATEGORY - C-ADMIN BACKEND (LIST) VIEWS BEGINS HERE ##
    #######################################################################

    path("sub-category", views.subCategory, name="subCategory"),

    ########################################################################
    ## MANAGE POSTS SUB CATEGORY C-ADMIN BACKEND (CRUD) VIEWS BEGINS HERE ##
    ########################################################################

    path("sub-category/create", views.subCategoryCreate, name="subCategoryCreate"),
    path("sub-category/<int:subcatid>/update", views.subCategoryUpdate, name="subCategoryUpdate"),
    path("sub-category/<int:subcatid>/delete", views.subCategoryDelete, name="subCategoryDelete"),
    path("sub-category/action", views.subCategoryBulkAction, name="subCategoryBulkAction"),

]

