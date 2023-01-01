# posts/forms.py

from django import forms
from .models import User, Post, PostCategory, PostSubCategory
from ckeditor.fields import RichTextField
from members.models import User

# Create your forms here.

action_choices = [('-1', 'Select Bulk Action'), ('trash', 'Move to Trash')]
admin_post_action_choices = [('-1', 'Select Bulk Action'), ('trash', 'Move to Trash'), ('published', 'Change Status to Publish'), ('pending review', 'Change Status to Pending Review')]
author_post_action_choices = [('-1', 'Select Bulk Action'), ('trash', 'Move to Trash')]

'''
def test(request):

    if request.user.role == 'admin':
        post_action_choices = [('-1', 'Select Bulk Action'), ('trash', 'Move to Trash'),
                               ('published', 'Change Status to Publish'),
                               ('pending review', 'Change Status to Pending Review')]
    else:
        post_action_choices = [('-1', 'Select Bulk Action'), ('trash', 'Move to Trash')]

    return post_action_choices
'''



class CategoryForm(forms.ModelForm):

    #id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = PostCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'cf2', 'class': 'form-control', 'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'id': 'cf3', 'class': 'form-control', 'placeholder': 'Category Description', 'rows': 6
            })
        }
        labels = {
            'name': 'Category Name',
            'description': 'Category Description',
        }





class SubCategoryForm(forms.ModelForm):

    class Meta:

        model = PostSubCategory
        fields = ['category', 'name', 'description']
        widgets = {
            'category': forms.Select(attrs={
                'id': 'scf2', 'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'id': 'scf3', 'class': 'form-control', 'placeholder': 'Sub Category Name'
            }),
            'description': forms.Textarea(attrs={
                'id': 'scf4', 'class': 'form-control', 'placeholder': 'Sub Category Description', 'rows': 2
            })
        }
        labels = {
            'category': 'Sub Category Parent',
            'name': 'Sub Category Name',
            'description': 'Sub Category Description',
        }





class BulkActionsForm(forms.Form):

    action = forms.CharField(widget=forms.Select(choices=action_choices, attrs={
        'id': 'baf1', 'class': 'form-select form-select-sm'
    }))
    select_all = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'select_all_cats', 'class': 'select_allbox'
    }))
    checked_id = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'select_all_cats', 'class': 'checkbox'
    }))





class PostBulkActionsForm(forms.Form):

    action = forms.ChoiceField(widget=forms.Select(attrs={
        'id': 'pbaf1', 'class': 'form-select form-select-sm'
    }))
    select_all = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'select_all_posts', 'class': 'select_allbox'
    }))
    checked_id = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'id': 'select_all_posts', 'class': 'checkbox'
    }))

    def __init__(self, current_user, *args, **kwargs):
        super(PostBulkActionsForm, self).__init__(*args, **kwargs)
        if current_user.role == 'admin':
            self.fields['action'].choices = admin_post_action_choices
        elif current_user.role == 'author':
            self.fields['action'].choices = author_post_action_choices







class PostForm(forms.ModelForm):

    agree = forms.BooleanField(label='Terms and Condition', required=True, widget=forms.CheckboxInput(attrs={
        'id': 'pf9', 'class': 'form-check-input', 'placeholder': "I Agree to all of the <a href='#'>Terms and Conditions</a>"
    }))

    class Meta:

        model = Post
        fields = ['heading', 'intro', 'title', 'category', 'sub_category', 'content', 'post_image', 'notify', 'agree']
        widgets = {
            'heading': forms.TextInput(attrs={
                'id': 'pf1', 'class': 'form-control', 'placeholder': 'e.g Loving Yourself The Way You Are'
            }),
            'intro': forms.Textarea(attrs={
                'id': 'pf2', 'class': 'form-control', 'placeholder': 'If your poem uses a poetic form or techniques tell us about it. The story behind your poem is you. We want to know this story. It will make your poem so much more meaningful. Tell us a little about yourself, what this poem means to you and why you wrote it.', 'rows': 4
            }),
            'title': forms.TextInput(attrs={
                'id': 'pf3', 'class': 'form-control', 'placeholder': "Your poem's title"
            }),
            'content': forms.Textarea(attrs={
                'id': 'pf4', 'class': 'form-control', 'placeholder': "Write your complete poem"
            }),
            'category': forms.Select(attrs={
                'id': 'pf5', 'class': 'form-select',
            }),
            'sub_category': forms.Select(attrs={
                'id': 'pf6', 'class': 'form-select',
            }),
            'post_image': forms.FileInput(attrs={
                'id': 'pf7', 'class': 'form-control', 'type': 'file'
            }),
            'notify': forms.CheckboxInput(attrs={
                'id': 'pf8', 'class': 'form-check-input', 'placeholder': "Notify me by email when comments are posted on my poem"
            }),
            #'agree': forms.CheckboxInput(attrs={
            #    'id': 'pf9', 'class': 'form-check-input', 'placeholder': "I Agree to all of the <a href='#'>Terms and Conditions</a>"
            #}),

        }
        labels = {
            'heading': 'Heading, What Is Your Poem About?',
            'intro': 'Introduction, What Is Your Story?',
            'title': 'Poem Title',
            'content': 'Write Your Full Poem Content',
            'category': 'Parent Category',
            'sub_category': 'Sub Category',
            'post_image': 'Post Featured Image',
            'notify': 'Comment Notifications',
            'agree': 'Terms and Condition'
        }
        help_texts = {
            'heading': 'One sentence Heading for your poem. (15 - 50 Characters)',
            'intro': 'Between 45 - 500 Characters',
            'title': 'Between 5 - 75 Characters',
            'content': 'Between 45 - 3000 Characters',
            'post_image': 'Accepted image dimension is width - 1280px by height - 640px',
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = PostSubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = PostSubCategory.objects.filter(category=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk and self.instance.category is not None:
            self.fields['sub_category'].queryset = self.instance.category.parentcategory.order_by('name')
