from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.views.generic import ListView
from django.shortcuts import render,get_object_or_404
from django.http import Http404

from .models import Post


class Postlistview(ListView):
    
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name='blog/post/list.html'


def post_detail(request, year, month, day, publish):
 
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=publish,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )





