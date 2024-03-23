from django.urls import path
from .views import PostListView, search_results

from . import views

app_name = 'filmblog'


urlpatterns = [
    path("", PostListView.as_view(), name="index"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('search/', search_results, name='search_results'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag')

]