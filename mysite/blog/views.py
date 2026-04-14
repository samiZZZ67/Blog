from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.views.generic import ListView
from django.shortcuts import render,get_object_or_404
from django.http import Http404
from .forms import EmailPostForm
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

def post_share(request,post_id):
    post=get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    if request.method=='POST':
        form=EmailPostForm(request.POST)

        if form.is_valid:
            cd=form.cleaned_data
    else:
        form=EmailPostForm()

    return render (
        request,
        'blog/post/share.html',
        {'forms':form},
        {'post':post}

    )





