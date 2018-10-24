from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
# A blog post
class Post(models.Model):
    # Only a super user can be author of a post
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    # Method is called to publish the post from draft or directly
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # Since a post is linked to the 'Comments' model so i guess self.comments refers
    # to the list of all comment models to which this post is a foriegn
    # so this method basically returns the comments on the post with 'approved_comment=True'
    # in it so that comments can be shown there using a filter
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # The method is called by the framework when this model is created
    # in a class based view
    def get_absolute_url(self):
        # we basically return to the post_detail view ;  specifying the primary key
        # once a 'Post' is created
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title


# A comment on a post
# It has a 'Post' associated with it using ForeignKey
# Anyone could comment on a blog post; no autherisation
# superuser could call a aprove method on comment to show up
class Comment(models.Model):
    post = models.ForeignKey('app.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    # Method called by the framework on creation of a 'Comment'
    def get_absolute_url(self):
        # return to the homepage since the comment will be pending for
        # super user aproovel
        return  reverse('post_list')

    def __str__(self):
        return self.text
