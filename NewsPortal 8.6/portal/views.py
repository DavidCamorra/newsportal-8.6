from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, User
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMultiAlternatives

from .filters import PostFilter
from django.template.loader import render_to_string


class NewsList(ListView):
    model = Post
    ordering = 'add_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_in_common'] = self.request.user.groups.filter(name='common').exists()
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    permission_required = 'portal.add_post'


class PostEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    permission_required = 'portal.change_post'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'flatpages/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class NewsListSearch(ListView):
    model = Post
    ordering = 'add_time'
    template_name = 'news_search.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe(request, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    for category in post.category.all():
        user = User.objects.get(pk=request.user.id)
        category.subscribers.add(user)

    return redirect('/news')


@login_required
def unsubscribe(request, **kwargs):
    category = Category.objects.get(pk=kwargs['pk'])
    user = request.user
    if user in category.subscribers.all():
        category.subscribers.remove(user)

    return redirect('/news')

