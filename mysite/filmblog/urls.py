from django.urls import path

from . import views

app_name = 'filmblog'


urlpatterns = [
    path("", views.index, name="index"),
    path("blog", views.post_list, name="2"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
	 name='post_detail'),
    path("single-standard.html", views.singl_test, name="test"),
]