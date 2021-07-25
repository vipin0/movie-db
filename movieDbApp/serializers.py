from django.db.models import fields
from movieDbApp.models import Movie, Review,StreamingPlatform
from rest_framework import serializers

class ReviewReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class ReviewWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Review
        # fields = ['rating','description','active']
        fields = '__all__'
        read_only_fields  = ['id','created','modified','movie']

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewReadSerializer(many=True,read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id','released_on']

class StreamingPlatformSerializer(serializers.ModelSerializer):

    movies = MovieSerializer(many=True,read_only=True) # gives everything
    
    # movies = serializers.StringRelatedField(many=True)   # returns only name

    # movies = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie_detail'
    # )
    
    class Meta:
        model = StreamingPlatform
        fields = '__all__'


# without model serializers
class MovieSerializer1(serializers.Serializer):
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
