# members/forms.py

from django import forms
from .models import User
from django.forms.widgets import NumberInput
# from django.contrib.auth.forms import PasswordChangeForm

# from allauth.account.forms import ChangePasswordForm

# Create your forms here.

user_action_choices = [('-1', 'Select Bulk Action'), ('author', 'Change Role to Author'), ('admin', 'Change Role to Admin'), ('pending email verification', 'Change Profile to Pending Email Verification'), ('pending profile activation', 'Change Profile to Pending Profile Activation'), ('profile activated', 'Change Profile to Profile Activated'), ('1', 'Activate User'), ('0', 'Deactivate User'), ('trash', 'Move to Trash')]

status_choices = [('', 'Filter By Status'), ('pending activation', 'Pending Activation'), ('active', 'Active'), ('inactive', 'Inactive')]

region_choices = [('africa', 'Africa'), ('antarctica', 'Antarctica'), ('asia', 'Asia'), ('australia', 'Australia'), ('europe', 'Europe'), ('north-america', 'North-America'), ('south-america', 'South-America')]

gender_choices = [('male', 'Male'), ('female', 'Female')]

role_choices = [('admin', 'Admin'), ('author', 'Author')]

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        'id': 'lf1', 'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(max_length=25, widget=forms.PasswordInput(attrs={
        'id': 'lf2', 'class': 'form-control', 'placeholder': 'Password'
    }))

    '''class Meta:

        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'lf1', 'class': 'form-control', 'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'id': 'lf2', 'class': 'form-control', 'placeholder': 'Password'
            }),
        }
        help_texts = {
            'username': ''
        }'''


class RegisterForm(forms.ModelForm):
    pass_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'rf6', 'class': 'form-control', 'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'rf1', 'class': 'form-control', 'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'rf2', 'class': 'form-control', 'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'rf3', 'class': 'form-control', 'placeholder': 'Email'
            }),
            'username': forms.TextInput(attrs={
                'id': 'rf4', 'class': 'form-control', 'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'id': 'rf5', 'class': 'form-control', 'placeholder': 'Password'
            }),
        }
        help_texts = {
            'username': ''
        }


class PersonalInfoForm(forms.ModelForm):
    birthday = forms.DateField(required=True, widget=NumberInput(attrs={'type': 'date', 'class': 'form-control'}))

    # birthday = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'profile_image', 'cover_image', 'birthday', 'phone_number', 'region',
                  'occupation', 'gender', 'religion', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'pif1', 'class': 'form-control', 'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'pif2', 'class': 'form-control', 'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'pif3', 'class': 'form-control', 'placeholder': 'Email'
            }),
            'username': forms.TextInput(attrs={
                'id': 'pif4', 'class': 'form-control', 'placeholder': 'Username'
            }),
            'profile_image': forms.FileInput(attrs={
                'id': 'pif5', 'class': 'form-control'
            }),
            'cover_image': forms.FileInput(attrs={
                'id': 'pif6', 'class': 'form-control'
            }),
            # 'birthday': DatePickerInput(options={
            #    "format": "MM/DD/YYYY", "showClose": True, "showClear": True, "showTodayButton": True,
            # }),
            'phone_number': forms.NumberInput(attrs={
                'id': 'pif8', 'class': 'form-control', 'placeholder': 'Phone Number'
            }),
            'region': forms.Select(choices=region_choices, attrs={
                'id': 'pif9', 'class': 'form-select', 'placeholder': 'Select Region'
            }),
            'occupation': forms.TextInput(attrs={
                'id': 'pif10', 'class': 'form-control', 'placeholder': 'Occupation'
            }),
            'gender': forms.Select(choices=gender_choices, attrs={
                'id': 'pif11', 'class': 'form-select', 'placeholder': 'Select Gender'
            }),
            'religion': forms.TextInput(attrs={
                'id': 'pif12', 'class': 'form-control', 'placeholder': 'Religion'
            }),
            'bio': forms.Textarea(attrs={
                'id': 'pif13', 'class': 'form-control', 'placeholder': 'Brief Bio', 'rows': 2
            })
        }
        help_texts = {
            'username': '',
            'profile_image': 'Accepted image dimension is width - 300px by height - 300px',
            'cover_image': 'Accepted image dimension is width - 1280px by height - 400px'
        }

    # def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['birthday'].widget.attrs.update({'class': 'form-control'})


class EducationHistoryForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['institution', 'degree', 'program', 'period', 'location', 'program_desc']
        widgets = {
            'institution': forms.TextInput(attrs={
                'id': 'ehf1', 'class': 'form-control', 'placeholder': 'e.g University of Middlesex'
            }),
            'degree': forms.TextInput(attrs={
                'id': 'ehf2', 'class': 'form-control', 'placeholder': 'e.g BSc. Computer Science'
            }),
            'program': forms.TextInput(attrs={
                'id': 'ehf3', 'class': 'form-control', 'placeholder': 'e.g Computer Science'
            }),
            'period': forms.TextInput(attrs={
                'id': 'ehf4', 'class': 'form-control', 'placeholder': 'e.g May, 2005 - June, 2010'
            }),
            'location': forms.TextInput(attrs={
                'id': 'ehf5', 'class': 'form-control', 'placeholder': 'e.g United Kingdom'
            }),
            'program_desc': forms.Textarea(attrs={
                'id': 'ehf6', 'class': 'form-control', 'placeholder': 'e.g Brief description of your program', 'rows': 2
            }),
        }
        help_texts = {
            'institution': ''
        }
        labels = {
            'institution': 'Institution Label'
        }


class SocialProfilesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['facebook', 'instagram', 'twitter', 'linkedin']
        widgets = {
            'facebook': forms.URLInput(attrs={
                'id': 'spf1', 'class': 'form-control', 'placeholder': 'e.g https://www.facebook.com/sammyleths',
                'ico': 'fab fa-facebook fa-md'
            }),
            'instagram': forms.URLInput(attrs={
                'id': 'spf2', 'class': 'form-control', 'placeholder': 'e.g https://www.instagram.com/sammyleths',
                'ico': 'fab fa-instagram fa-md'
            }),
            'twitter': forms.URLInput(attrs={
                'id': 'spf3', 'class': 'form-control', 'placeholder': 'e.g https://www.twitter.com/sammyleths',
                'ico': 'fab fa-twitter fa-md'
            }),
            'linkedin': forms.URLInput(attrs={
                'id': 'spf4', 'class': 'form-control', 'placeholder': 'e.g https://www.linkedin.com/sammyleths',
                'ico': 'fab fa-linkedin fa-md'
            }),
        }
        help_texts = {
            'facebook': ''
        }


# PURE CUSTOM PASSWORD CHANGE FORM

'''class ChangePasswordForm(forms.ModelForm):

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'cpf2', 'class': 'form-control', 'placeholder': 'New Password'
    }))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'cpf3', 'class': 'form-control', 'placeholder': 'Confirm New Password'
    }))

    class Meta:

        model = User
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={
                'id': 'cpf1', 'class': 'form-control', 'placeholder': 'Current Password'
            }),
        }
        labels = {
            'password': 'Current Password'
        }
        '''


# DJANGO AUTH CHANGE PASSWORD FORM

'''
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={
        'id': 'pwcf1', 'class': 'form-control', 'type': 'password', 'placeholder': 'Old/Current Password'
    }))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={
        'id': 'pwcf2', 'class': 'form-control', 'type': 'password', 'placeholder': 'New Password'
    }))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={
        'id': 'pwcf3', 'class': 'form-control', 'type': 'password', 'placeholder': 'Confirm New Password'
    }))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
'''



# DJANGO ALLAUTH CHANGE PASSWORD FORM

'''
class MyCustomChangePasswordForm(ChangePasswordForm):

    def save(self):

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomChangePasswordForm, self).save()

        # Add your own processing here.

'''




class BulkActionsForm(forms.Form):

    action = forms.CharField(widget=forms.Select(choices=user_action_choices, attrs={
        'id': 'ubaf1', 'class': 'form-select form-select-sm'
    }))
    select_all = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'select_all_users', 'class': 'select_allbox'
    }))
    checked_id = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'select_all_users', 'class': 'checkbox'
    }))





class UserFilterForm(forms.Form):

    filter = forms.ChoiceField(choices=status_choices, required=False, widget=forms.Select(attrs={'class': 'form-control custom-select custom-select-sm'}))



class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['role', 'is_active']
        widgets = {
            'role': forms.Select(choices=role_choices, attrs={
                'id': 'usf1', 'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'id': 'usf1', 'class': 'form-check-input', 'type': 'checkbox', 'placeholder': 'Is Active'
            }),
        }