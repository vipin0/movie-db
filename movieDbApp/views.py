from django.http import response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view     # function based view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from movieDbApp.pagination import CustomPagination
from movieDbApp.permissions import IsAdminOrReadOnly, ReviewUserOrReadOnly
from movieDbApp.models import Movie, Star,StreamingPlatform,Review
from movieDbApp.serializers import MovieReadSerializer, MovieWriteSerializer, ReviewReadSerializer, ReviewWriteSerializer, StarSerializer,StreamingPlatformSerializer, ReviewSerializer
# Create your views here.

#  using genrics view

class MovieList(ListCreateAPIView):
    # serializer_class = MovieReadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name','=platform__name','stars__full_name']
    ordering_fields = ['average_rating', 'platform','released_on']
    
    def get_queryset(self):
        return Movie.objects.prefetch_related('stars').select_related('platform').prefetch_related('reviews').all()
    def get_serializer_class(self):

        if self.request.method == 'POST':
            return MovieWriteSerializer
        return MovieReadSerializer

class MovieDetail(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return MovieWriteSerializer
        return MovieReadSerializer

class StreamingPlatformList(ListCreateAPIView):

    serializer_class = StreamingPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

    def get_queryset(self):
        return StreamingPlatform.objects.prefetch_related('movies').all()

class StreamingPlatformDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = StreamingPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return StreamingPlatform.objects.all()

class ReviewList(ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['rating', 'review_user__username']
    search_fields = ['description','=review_user__username','movie__name']
    ordering_fields = ['rating']
    
    def get_queryset(self):
        print(self.request)
        movie_id = self.kwargs['movie_id']
        movie = Movie.objects.get(pk=movie_id)
        return Review.objects.filter(movie=movie)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewWriteSerializer
        return ReviewReadSerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs['movie_id']
        movie = Movie.objects.get(pk=pk)
        user = self.request.user
        is_reviewed = Review.objects.filter(movie=movie,review_user=user)
        if is_reviewed.exists():
            raise ValidationError("You have already reviewed this movie!",400)
        
        if movie.average_rating == 0:
            movie.average_rating = serializer.validated_data['rating']
        else:
            movie.average_rating = (movie.average_rating + serializer.validated_data['rating'])/2

        movie.number_rating += 1
        movie.save()
        serializer.save(movie=movie,review_user=user)

class ReviewDetail(RetrieveUpdateDestroyAPIView):
    
    queryset = Review.objects.all()
    permission_classes = [ReviewUserOrReadOnly]

    def get_serializer_class(self):
        
        if self.request.method in ('PUT','PATCH'):
            return ReviewWriteSerializer
        return ReviewReadSerializer

class ActorList(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StarSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter,]
    search_fields = ['full_name',]

    def get_queryset(self):
        return Star.objects.all()

class ActorDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StarSerializer

    def get_queryset(self):
        return Star.objects.all()


    # tried getting movies of each actor

    # def get(self,request,pk):
    #     actor = Star.objects.get(pk=pk)
    #     movies = Movie.objects.filter(stars=actor)
    #     m_serialzer = MovieReadSerializer(movies,many=True)
    #     print(m_serialzer.data)
    #     response = StarSerializer(actor)
    #     response.data['movies']= m_serialzer.data
    #     return Response(response.data,status=status.HTTP_200_OK)


# using APIView class based

class MovieListAV(APIView):

    def get(self,request):
        movies = Movie.objects.all()
        serializer = MovieReadSerializer(movies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = MovieReadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MovieDetailAV(APIView):

    def get(self,request,pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist as e:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = MovieReadSerializer(movie)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist as e:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = MovieReadSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist as e:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response({'message':'Movie deleted'},status=status.HTTP_204_NO_CONTENT)

class StreamingPlatformListAV(APIView):

    def get(self,request):
        streamingPlateforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(streamingPlateforms,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class StreamingPlatformDetailAv(APIView):

    def get(self,request,pk):
        try:
            plateform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist as e:
            return Response({'error':'StreamingPlatform not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(plateform)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        try:
            plateform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist as e:
            return Response({'error':'StreamingPlatform not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(plateform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,pk):
        try:
            plateform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist as e:
            return Response({'error':'StreamingPlatform not found'},status=status.HTTP_404_NOT_FOUND)
        plateform.delete()
        return Response({'message':'StreamingPlatform deleted'},status=status.HTTP_204_NO_CONTENT)

class ReviewAV(APIView):

    def get(self,request,movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist as e:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,movie_id):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ReviewDetailAV(APIView):

    def get(self,request,movie_id,pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist as e:
            return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,movie_id,pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist as e:
            return Response({'error':'StreamingPlatform not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,movie_id,pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist as e:
            return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({'message':'Review deleted'},status=status.HTTP_204_NO_CONTENT)

# ************** function based view **************
@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieReadSerializer(movies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieReadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def movie_detail(request,pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist as e:
        return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MovieReadSerializer(movie)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = MovieReadSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie.delete()
        return Response({'message':'Movie deleted'},status=status.HTTP_204_NO_CONTENT)
    