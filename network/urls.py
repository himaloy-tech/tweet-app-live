
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="NewPost"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("obj/<int:id>", views.obj, name="obj"),
    path("edit", views.edit, name="edit"),
    path("like/<int:id>/<str:current_user>", views.like, name="like"),
    path("unlike/<int:id>/<str:current_user>", views.unlike, name="unlike")
]
