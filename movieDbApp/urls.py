from django.urls import path
from movieDbApp import views
urlpatterns = [
    path('movies/',view=views.MovieList.as_view(),name='movie_list'),
    path('movies/<int:pk>/',view=views.MovieDetail.as_view(),name='movie_detail'),
    
    # url = movie/<movie_id>review
    path('movies/<int:movie_id>/review/',views.ReviewList.as_view(),name='review-list'),
    
    # url = movie/<movie_id>review/<review_id>
    path('movies/<int:movie_id>/review/<int:pk>/',views.ReviewDetail.as_view(),name='review-detail'),
    
    path('streams/',views.StreamingPlatformList.as_view(),name="streaming_list"),
    path('streams/<int:pk>/',views.StreamingPlatformDetail.as_view(),name="streaming_detail"),
]
