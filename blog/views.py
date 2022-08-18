from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

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
