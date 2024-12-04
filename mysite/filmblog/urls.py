from django.urls import path
from .views import PostListView, search_results, PostCreateView, PostManageView

from . import views

app_name = 'filmblog'


urlpatterns = [
    path("", PostListView.as_view(), name="index"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('search/', search_results, name='search_results'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/manage/', PostManageView.as_view(), name='post_manage'),
    path('post/<slug:slug>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),


]