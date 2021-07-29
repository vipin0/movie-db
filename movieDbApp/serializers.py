from django.core.paginator import Paginator
from rest_framework import serializers
from movieDbApp.models import Movie, Review, Star,StreamingPlatform


class ReviewReadSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True) 
    class Meta:
        model = Review
        fields = '__all__'


class ReviewWriteSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    movie = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model =  Review
        # fields = ['rating','description','active']
        fields = '__all__'
        read_only_fields  = ['id','review_user','created','modified','movie','active']


class MovieWriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id','released_on','average_rating','number_rating']

class MovieReadSerializer(serializers.ModelSerializer):
    # reviews = ReviewReadSerializer(many=True,read_only=True)
    # reviews = serializers.StringRelatedField(many=True,read_only=True)
    # reviews = serializers.SerializerMethodField('paginated_reviews')
    total_reviews = serializers.SerializerMethodField('reviews_count')
    platform = serializers.StringRelatedField(read_only=True)
    stars = serializers.StringRelatedField(many=True)
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id','released_on','average_rating','number_rating']

    def reviews_count(self,obj):
        review = Review.objects.filter(movie=obj)
        return len(review)

    def paginated_reviews(self, obj):
        try:
            page_size = self.context.get('request').query_params.get('size')
        except Exception as e:
            page_size = 10
        if page_size is None:
            page_size = 10
        # page_size = self.context.get('request').query_params.get('size') or 10
        paginator = Paginator(obj.review.all(), page_size)
        try:
            page = self.context.get('request').query_params.get('page')
        except Exception as e:
            page = 1
        # page = self.context.get('request').query_params.get('page') or 1
        if page is None:
            page = 1
        review = paginator.page(page)
        serializer = MovieReadSerializer(review, many=True)
        return serializer.data

    

class StreamingPlatformSerializer(serializers.ModelSerializer):

    # movies = MovieReadSerializer(many=True,read_only=True) # gives everything

    # movies = serializers.SerializerMethodField('paginated_movies')
    
    # movies = serializers.StringRelatedField(many=True,read_only=True)   # returns only name

    movies = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie_detail'
    )
    
    class Meta:
        model = StreamingPlatform
        fields = '__all__'

    def paginated_movies(self, obj):
        page_size = self.context['request'].query_params.get('size') or 10
        paginator = Paginator(obj.movies.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1

        movie = paginator.page(page)
        serializer = MovieReadSerializer(movie, many=True)
        return serializer.data


class StarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Star
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


# without model serializers
class MovieReadSerializer1(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    released_on = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.active = validated_data.get('active',instance.active)
        instance.save()
        return instance

    # for name
    def validate_name(self, attrs):
        return super().validate(attrs)

    # for all
    def validate(self, attrs):
        return super().validate(attrs)
