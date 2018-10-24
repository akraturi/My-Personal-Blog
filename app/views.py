from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import (TemplateView , ListView,
                                 DetailView , CreateView,
                                 DeleteView , UpdateView)
from app.models import Post,Comment
# acts as a login_required decorator for class based views
from django.contrib.auth.mixins import LoginRequiredMixin
# decorator used with function based views , indicating that the user
# needs to be authenticated to perform certain action
from django.contrib.auth.decorators import login_required

from app.forms import PostForm,CommentForm
from  django.urls import reverse_lazy

# COMMENTS


# Create your views here.

# templateview child class deals with some html file
# to be shown maybe with some sort of templates in it
# which could dynamically be filled.
class AboutView(TemplateView):
    template_name = 'about.html'

# Represents the home page containing the list of blogs
class PostListView(ListView):
    # context_object_name = 'CONTEXT_OBJECT_NAME'
    model = Post
    # page_kwarg = 'page'
    # paginate_by =
    # template_name = 'TEMPLATE_NAME'

    # This super class method called to return the list of objects
    # we override this method to return the list of post in specific manner using some short of
    # query
    # we filter the objects using the published date i.e latest post should be on the top
   # __lte represents less than or equal to (<=)
    def get_queryset(self):
        # MORE EXPLAINATION : # filter by (fieldname_LOOKUPTYPE) here LOOKUPTYPE is 'lte'
        # eventually this translates to
        # SELECT * FROM POST  WHERE published_date <= Date.now() , something like this
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

# Displaying a post

class PostDetailView(DetailView):
    model = Post
    # slug_field = 'SLUG_FIELD'
    # slug_url_kwarg = 'SLUG_URL_KWARG'
    # success_url = 'SUCCESS_URL'
    # template_name = 'TEMPLATE_NAME'

# view specified for the creation of a post
# An example of multiple inheritance wow!
# LoginRequiredMixin indicates the login_required to perform this action
class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    # variables from superclass LoginRequiredMixin
    login_url ='/login/'
    redirect_field_name= 'app/post_detail.html'

    # form to be shown for the creation of the model Post
    form_class = PostForm

# update a blog post
class PostUpdateView(UpdateView,LoginRequiredMixin):
    model = Post
    # variables from superclass LoginRequiredMixin
    login_url ='/login/'
    redirect_field_name= 'app/post_detail.html'

    # form to be shown for the creation of the model Post
    form_class = PostForm

# Deleting a post
class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    # where it should go after deletion
    # success_url should not be activated be before deletion so reverse_lazy is used
    success_url = reverse_lazy('post_list')

# Draft list
class DraftListView(ListView,LoginRequiredMixin):
    model = Post
    login_url='/login/'
    redirect_field_name ='app/post_list.html'


    def get_queryset(self):
        # translates to
        # list all the posts which are not published yet
        # (SELECT * FROM POST WHERE published_date = NULL )
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

########################################################
########################################################
########################################################
 # COMMENTS with function based views
##########################################################

# Adding comment
# @login_required
def add_comment_to_post(request,pk):
    # grab the 'post' object corresponding
    # to comment object if exsits using primary key
    post = get_object_or_404(Post,pk=pk)

    # if the form is submited
    if request.method == 'POST':
        # get the filled form
        form = CommentForm(request.POST)
        if form.is_valid():
            # save the comment but do not commit
            comment = form.save(commit=False)
            # attach the corresponding post to it
            comment.post = post
            # save the comment now
            comment.save()
            # return to the post detail
            return redirect('post_detail',pk = post.pk)
    else:
        # if form was not submitted create a new form there
        form = CommentForm()
        # render the view
    return render(request,'app/comment_form.html',{'form':form})

# Aprovel of a comment
@login_required
def comment_approve(request,pk):
    # grab the comment
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk= comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    # delete from db
    comment.delete()
    return redirect('post_detail',pk=post_pk)

#  function based view for publishing the post not related to comments
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk = pk)
