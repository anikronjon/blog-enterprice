from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


# Create your views here.
def post_list_view(request):
    post_list = Post.publish.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        'posts': posts
    }
    return render(request, 'blog/post/post_list.html', context)


def post_detail_view(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISH,
        slug=post,
        published__year=year,
        published__month=month,
        published__day=day

    )
    context = {
        'post': post
    }
    return render(request, 'blog/post/post_detail.html', context)
