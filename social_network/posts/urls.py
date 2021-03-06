from django.urls import path
from . import views


urlpatterns = [
	path('create/', views.CreatePostAPIView.as_view(), name='create_post'),
	path('like-unlike/<int:pk>/', views.LikeUnlikeAPIView.as_view(), name='like_unlike'),
	path('analytics/', views.LikesAnalyticsListAPIView.as_view(), name='analytics'),
]