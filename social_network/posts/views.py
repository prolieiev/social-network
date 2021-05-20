from .models import Post, LikeDetail
from .serializers import PostSerializer
from datetime import datetime, timedelta
from django.db.models import Q, Sum, Count
from django.shortcuts import render
from django.utils import timezone
from rest_framework.generics import CreateAPIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreatePostAPIView(CreateAPIView):
		queryset = Post.objects.all()
		permission_classes = [IsAuthenticated]
		serializer_class = PostSerializer

		def perform_create(self, serializer):
				serializer.save(author=self.request.user)


class LikeUnlikeAPIView(APIView):
		permission_classes = [IsAuthenticated]

		def get_object(self, pk):
			try:
					return Post.objects.get(pk=pk)
			except Post.DoesNotExist:
					return Response(
							{'detail': 'Post not found.'}, 
							status=status.HTTP_400_BAD_REQUEST
					)

		def post(self, request, *args, **kwargs):
				post = self.get_object(kwargs.get('pk'))
				post.like.add(request.user)
				post.save()
				return Response({'detail': 'Like added.'})

		def delete(self, request, *args, **kwargs):
				post = self.get_object(kwargs.get('pk'))
				post.like.remove(request.user)
				post.save()
				return Response({'detail': 'Like removed.'})


class LikesAnalyticsListAPIView(APIView):
		permission_classes = [IsAuthenticated]

		def get(self, request, *args, **kwargs):
				date_from = request.GET.get('date_from', None)
				date_to = request.GET.get('date_to', None)
				if date_from == None or date_to == None:
						return Response(
							{'detail': 'Please provide both date_from and date_to parameters.'},
							status=status.HTTP_400_BAD_REQUEST
						)
				date_from = datetime.strptime(date_from, '%Y-%m-%d')
				date_to = datetime.strptime(date_to, '%Y-%m-%d')
				qs = Post.objects.filter(
					likedetail__created__gte=date_from, 
					likedetail__created__lte=date_to
				).distinct()
				response_data = {}
				while date_from <= date_to:
						date = date_from.strftime('%Y-%m-%d')						
						if count == 1:
								response_data[date] = f'{count} like'
						else:
								response_data[date] = f'{count} likes'
						date_from += timedelta(days=1)
				return Response(response_data)
		