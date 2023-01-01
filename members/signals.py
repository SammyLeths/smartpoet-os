from allauth.account.signals import email_confirmed, user_signed_up
from django.dispatch import receiver
from members.models import User, Profile


@receiver(email_confirmed)
def set_email_status(request, email_address, **kwargs):

    new_user = User.objects.get(email=email_address.email)
    new_user.status = 'pending profile activation'
    new_user.save()


@receiver(user_signed_up)
def create_user_profile(request, user, **kwargs):

    profile = Profile()
    profile.user = user
    profile.save()
