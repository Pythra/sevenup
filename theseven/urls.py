from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_form'),
    path('post/<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDelete.as_view(), name='post_confirm_delete'),
    path('comment/<int:pk>/', views.comment_detail, name='comment_detail'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_confirm_delete'),
    path('reply/<int:pk>/update/', views.ReplyUpdate.as_view(), name='reply_update'),
    path('reply/<int:pk>/delete/', views.ReplyDelete.as_view(), name='reply_confirm_delete'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.update_profile, name='profile'),
    path('search/results/blog/', views.search, name='blog_search_home'),
    path('notifications/replies/', views.reply_notifications, name='rep_notifications'),
    path('notifications/comments/', views.comment_notifications, name='com_notifications'),
    path('notifications/mentions/', views.mention_notifications, name='men_notifications'),
]
