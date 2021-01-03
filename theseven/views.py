import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
import datetime
from django.views.generic import DetailView, UpdateView, DeleteView, View, RedirectView
from .forms import CommentForm, PostForm, ProfileForm, ReplyForm, UserRegisterForm
from .models import Post, Comment, Reply, Profile


def post_list(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(posts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    date = datetime.datetime.now()
    context = {'posts': posts, 'current_date': date, 'page_obj': page_obj}
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'posts': posts,
                   'current_date': date, 'page_obj': page_obj}
    return render(request, 'milk/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.visits = post.visits + 1
    post.save()
    comments = post.comments.order_by('-created_on')
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))
    else:
        form = CommentForm()
    context = {'form': form, 'post': post, 'slug': slug, 'comments': comments, 'visits': post.visits,
               }
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'form': form, 'post': post, 'slug': slug, 'comments': comments, 'visits': post.visits,
                   }
    return render(request, 'milk/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()
    context = {'form': form}
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'form': form}
    return render(request, 'milk/post_form.html', context)


class PostUpdate(UpdateView):
    template_name = 'milk/post_update.html'
    model = Post
    form_class = PostForm


class PostDelete(DeleteView):
    template_name = 'milk/post_confirm_delete.html'
    model = Post
    success_url = reverse_lazy('home')


class CommentUpdate(UpdateView):
    template_name = 'milk/comment_edit.html'
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        comment = Comment.objects.get(pk=pk)
        post = comment.post
        return reverse('post_detail', kwargs={"slug": post.slug})


class CommentDelete(DeleteView):
    template_name = 'milk/comment_confirm_delete.html'
    model = Comment

    def get_success_url(self):
        pk = self.kwargs["pk"]
        comment = Comment.objects.get(pk=pk)
        post = comment.post
        return reverse('post_detail', kwargs={"slug": post.slug})


class ReplyUpdate(UpdateView):
    template_name = 'milk/reply_edit.html'
    model = Reply
    form_class = ReplyForm

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('comment_detail', kwargs={"pk": pk})


class ReplyDelete(DeleteView):
    template_name = 'milk/reply_confirm_delete.html'
    model = Reply
    success_url = reverse_lazy('home')


@login_required
def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    profile = Profile.objects.get(user=request.user)
    profile.visits = profile.visits + 1
    profile.save()
    if profile.visits == 1:
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, f'Your account has been updated!')
                return HttpResponseRedirect(reverse('profile_detail', kwargs={'pk': request.user.id}))

        else:
            profile_form = ProfileForm(instance=request.user.profile)

        context = {
            'p_form': profile_form
        }

        if request.user.is_authenticated:
            note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
                name=request.user)
            note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
                name=request.user)
            note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
            context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                       'p_form': profile_form
                       }
        return render(request, 'milk/profile_update.html', context)

    my_posts = Post.objects.filter(creator=user)[:5]
    my_comments = Comment.objects.filter(name=user)
    context = {'user': user, 'posts': my_posts, 'my_comments': my_comments}

    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'user': user, 'posts': my_posts, 'my_comments': my_comments}
    return render(request, 'milk/profile_detail.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return HttpResponseRedirect(reverse('profile_detail', kwargs={'pk': request.user.id}))

    else:
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'p_form': profile_form
    }

    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'p_form': profile_form
                   }
    return render(request, 'milk/profile_update.html', context)


def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    replies = comment.replies.all
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.name = request.user
            reply.save()
            return HttpResponseRedirect(reverse('comment_detail', kwargs={'pk': pk}))
    else:
        form = ReplyForm()
    context = {'form': form, 'comment': comment, 'replies': replies, 'pk': pk}
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'form': form, 'comment': comment, 'replies': replies, 'pk': pk}
    return render(request, 'milk/comment_detail.html', context)


def search(request):
    query = request.GET.get('b')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    comments = Comment.objects.filter(Q(body__icontains=query))
    context = {'posts': posts, 'comments': comments, 'query': query}
    if request.user.is_authenticated:
        note_comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
            name=request.user)
        note_mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
            name=request.user)
        note_replies = Reply.objects.filter(comment__name=request.user, not_status='unseen')
        context = {'note_comments': note_comments, 'note_mentions': note_mentions, 'note_replies': note_replies,
                   'posts': posts, 'comments': comments, 'query': query}
    return render(request, 'milk/search_home.html', context)


@login_required
def reply_notifications(request):
    mentions = Comment.objects.filter(body__icontains=request.user, not_status='unseen').exclude(
        name=request.user).order_by('-created_on')
    comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
        name=request.user).order_by('-created_on')
    replies = Reply.objects.filter(comment__name=request.user).order_by('-created_on')
    replies.update(not_status='seen')
    context = {'nmentions': mentions, 'ncomments': comments, 'nreplies': replies}
    return render(request, 'milk/notifications/reply_notifications.html', context)


@login_required
def comment_notifications(request):
    mentions = Comment.objects.filter(body__icontains=request.user.username, not_status='unseen').exclude(
        name=request.user).order_by(
        '-created_on')
    replies = Reply.objects.filter(comment__name=request.user, not_status='unseen').order_by('-created_on')
    comments = Comment.objects.filter(post__creator=request.user).exclude(
        name=request.user).order_by('-created_on')
    comments.update(not_status='seen')
    context = {'nmentions': mentions, 'ncomments': comments, 'nreplies': replies}
    return render(request, 'milk/notifications/comment_notifications.html', context)


@login_required
def mention_notifications(request):
    comments = Comment.objects.filter(post__creator=request.user, not_status='unseen').exclude(
        name=request.user).order_by('-created_on')
    replies = Reply.objects.filter(comment__name=request.user, not_status='unseen').order_by('-created_on')
    mentions = Comment.objects.filter(body__icontains=request.user).exclude(
        name=request.user).order_by('-created_on')
    mentions.update(not_status='seen')
    context = {'nmentions': mentions, 'ncomments': comments, 'nreplies': replies}
    return render(request, 'milk/notifications/mention_notifications.html', context)


class SignUpView(View):
    form_class = UserRegisterForm
    template_name = 'milk/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            return redirect('login')

        return render(request, self.template_name, {'form': form})
