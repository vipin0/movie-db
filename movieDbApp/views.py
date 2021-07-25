from django.http import response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view     # function based view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from movieDbApp.permissions import ReviewUserOrReadOnly
from movieDbApp.models import Movie,StreamingPlatform,Review
from movieDbApp.serializers import MovieSerializer, ReviewReadSerializer, ReviewWriteSerializer,StreamingPlatformSerializer, ReviewSerializer
# Create your views here.





# using APIView class based

class MovieListAV(APIView):

    def get(self,request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer = MovieSerializer(data=request.data)
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
        serializer = MovieSerializer(movie)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist as e:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie,data=request.data)
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

    def get(self,request,mpk):
        try:
            movie = Movie.objects.get(pk=mpk)
        except Movie.DoesNotExist as e:
            return Response({'error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,mpk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ReviewDetailAV(APIView):

    def get(self,request,mpk,pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist as e:
            return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,mpk,pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist as e:
            return Response({'error':'StreamingPlatform not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,mpk,pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist as e:
            return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({'message':'Review deleted'},status=status.HTTP_204_NO_CONTENT)

# review using genrics view

class ReviewList(ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        print(self.request)
        mpk = self.kwargs['mpk']
        movie = Movie.objects.get(pk=mpk)
        return Review.objects.filter(movie=movie)
    def get_serializer_class(self):
        
        if self.request.method == 'POST':
            return ReviewWriteSerializer
        return ReviewReadSerializer
    def perform_create(self, serializer):
        pk = self.kwargs['mpk']
        movie = Movie.objects.get(pk=pk)
        user = self.request.user
        is_reviewed = Review.objects.filter(movie=movie,review_user=user)
        if is_reviewed.exists():
            raise ValidationError("You have already reviewed this movie!",400)
        serializer.save(movie=movie,review_user=user)

        
    

class ReviewDetail(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [ReviewUserOrReadOnly]
    def get_serializer_class(self):
        
        if self.request.method in ('PUT','PATCH'):
            return ReviewWriteSerializer
        return ReviewReadSerializer


# ************** function based view **************
@api_view(['GET','POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
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
        serializer = MovieSerializer(movie)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        movie.delete()
        return Response({'message':'Movie deleted'},status=status.HTTP_204_NO_CONTENT)
    