import operator
from _functools import reduce

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, RedirectView
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 3
    queryset = Post.objects.all()


class PostSearchListView(PostListView):
    paginate_by = 3

    def get_queryset(self):
        result = super(PostSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.or_, (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.or_, (Q(body__icontains=q) for q in query_list)) |
                reduce(operator.or_, (Q(author__city__icontains=q) for q in query_list)) |
                reduce(operator.or_, (Q(author__country__icontains=q) for q in query_list))
            )

        return result


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        user = self.request.user.profile
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return '/net/'


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post_id)
    page = request.GET.get('page', 1)
    paginator = Paginator(comments, 3)
    try:
        comments_list = paginator.page(page)
    except PageNotAnInteger:
        comments_list = paginator.page(1)
    except EmptyPage:
        comments_list = paginator.page(paginator.num_pages)
    context = {
        "post": post,
        "comments_list": comments_list,
    }
    return render(request, "post.html", context)
