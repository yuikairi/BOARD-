from django.urls import path
from . import views
from .views import CreatePostView,PostDeleteView,ranking_view

app_name = 'boards'
urlpatterns = [
    path('post_list/', views.post_list, name='post_list'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('school_list/', views.school_list, name='school_list'),
    path('post/<int:school_id>/<int:city_id>/', views.CreatePostView.as_view(), name='post'),
    path('', views.IndexView.as_view(), name='index'),
    path('search_school/', views.search_school, name='search_school'),
    path('school/<int:school_id>/', views.school_detail, name='school_detail'),
    path('ranking', views.ranking_view, name='ranking'), 
    path('boards/post_done/<int:school_id>/<int:city_id>/', views.PostSuccessView.as_view(),name='post_done'),
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('delete_success/', views.DeleteSuccessView.as_view(), name='delete_success'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
]