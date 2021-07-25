from django.urls import path
from movieDbApp import views
urlpatterns = [
    path('',view=views.MovieListAV.as_view(),name='movie_list'),
    path('<int:pk>',view=views.MovieDetailAV.as_view(),name='movie_detail'),
    path('streams/',views.StreamingPlatformListAV.as_view(),name="streaming_list"),
    path('streams/<int:pk>',views.StreamingPlatformDetailAv.as_view(),name="streaming_detail"),
    
    # url = movie/<movie_id>review/<review_id>
    path('<int:mpk>/review/<int:pk>',views.ReviewDetail.as_view(),name='review-detail'),

    # url = movie/<movie_id>review
    path('<int:mpk>/review/',views.ReviewList.as_view(),name='review-list'),
    
]
