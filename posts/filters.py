# posts/filters.py

from posts.models import Post, PostCategory, PostSubCategory
import django_filters

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['published_date', 'category', 'sub_category', 'status', 'author']



class PostCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = PostCategory
        fields = ['name']



class PostSubCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = PostSubCategory
        fields = ['name', 'category']