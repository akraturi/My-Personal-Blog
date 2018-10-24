from django import forms
from app.models import Post,Comment

# These form classes inherits from ModelForm which
# allows us to directly create forms with the defined
# model
# An inline class(inner class) 'Meta' is to be defined
# to define the model for which the form is to be created
# and the fields of the model which should or shouldn't be
# presented in the form.(e.g creation_date should not be decided by
# by the end user)
# finally these form class instances are created inside the
# view classes or functions so they are genrated dynamically

class PostForm(forms.ModelForm):

    class Meta():
        # connect model to the form
        model = Post
        # specify the fields to be displayed
        fields = ('author','title','text')
        # Styling the dynamically generated html
        # a dictionary named 'widgets' needs to be defined which contains
        # the model fields corresponding to the form as key and some value as shownself.
        # now the css class names are passed as value to the key 'class' as shown
        # it could be our own css classes or from some third party lib ;

        # e.g- textinputclass is our own css class and while medium-editor-textarea comes
        # from medium third party library.

        widgets = {
           'title':forms.TextInput(attrs={'class':'textinputclass'}),
           'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        widgets = {
           'author':forms.TextInput(attrs={'class':'textinputclass'}),
           'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
