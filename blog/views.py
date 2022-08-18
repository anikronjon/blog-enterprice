from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from .forms import EmailPostForm
from .models import Post


# Create your views here.
class PostListView(ListView):
    queryset = Post.publish.select_related('author').all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'blog/post/post_list.html'

    def paginate_queryset(self, queryset, page_size):
        try:
            return super(PostListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            self.kwargs['page'] = 1
            return super(PostListView, self).paginate_queryset(queryset, page_size)


def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(Post, published__year=year, published__month=month, published__day=day, slug=post, status=Post.Status.PUBLISH)
    context = {
        'post': post
    }
    return render(request, 'blog/post/post_detail.html', context)


# Post Share by Email
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISH)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            to = form.cleaned_data['to']
            comment = form.cleaned_data['comments']
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{name} share you {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {name}\'s comments:{comment}"
            send_mail(subject, message, "youremail@gmail.com", [to])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
