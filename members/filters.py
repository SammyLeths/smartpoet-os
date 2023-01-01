# members/filters.py

from members.models import User
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'status', 'is_active']