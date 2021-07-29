from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase
from rest_framework import status

from movieDbApp import models
# Create your tests here.

class StreamingPlatformTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test",password="Test@1234")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamingPlatform.objects.create(
                                                                name="netflix",
                                                                about="netflix",
                                                                website="netflix.com"
                                                            )

    
    def test_streamingplatform_create(self):
        data={
            "name":"netflix",
            "about":"netflix",
            "website":"netflix.com"
        } 
        response = self.client.post(reverse('streaming_list'),data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_streamingplatform_list(self):
        response = self.client.get(reverse('streaming_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamingplatform_get_one(self):
        response = self.client.get(reverse('streaming_detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamingplatform_put(self):
        data={
            "name":"netflix",
            "about":"netflix --update",
            "website":"netflix.com"
        } 
        response = self.client.put(reverse('streaming_detail',args=(self.stream.id,)),data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_streamingplatform_delete(self):
        response = self.client.delete(reverse('streaming_detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


class MovieTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",password="Test@1234")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        actors = [models.Star(full_name='Test1',about="Test1"),models.Star(full_name='Test2',about="Test2"),]

        self.actors = models.Star.objects.bulk_create(actors)
        self.stream = models.StreamingPlatform.objects.create(
                                                                name="netflix",
                                                                about="netflix",
                                                                website="netflix.com"
                                                            )
        self.movie = models.Movie.objects.create(
                                                name="TestMovie",
                                                description="TEst",
                                                active= True,
                                                platform=self.stream
                                            )
        # self.movie.stars.set(self.actors)
    
    def test_movie_create(self):
        data = {
                "name": "TestMovie",
                "description": "TEst --updated",
                "active": True,
                "platform": self.stream.id,
                "stars": ''
            }
        response = self.client.post(reverse('movie_list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_movie_list(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_movie_get_one(self):
        response = self.client.get(reverse('movie_detail',args=(self.movie.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_movie_put(self):
        data = {
                "name": "TestMovie",
                "description": "TEst --updated",
                "active": True,
                "platform": self.stream
            }
        response = self.client.put(reverse('movie_detail',args=(self.movie.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_movie_delete(self):
        response = self.client.delete(reverse('movie_detail',args=(self.movie.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",password="Test@1234")
        self.user1 = User.objects.create_user(username="test1",password="Test@1234")
        
        self.token = Token.objects.get(user__username=self.user)
        self.token1 = Token.objects.get(user__username=self.user1)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamingPlatform.objects.create(
                                                                name="netflix",
                                                                about="netflix",
                                                                website="netflix.com"
                                                            )
        self.movie = models.Movie.objects.create(
                                                name="TestMovie",
                                                description="TEst",
                                                active= True,
                                                platform=self.stream
                                            )
        self.review = models.Review.objects.create(
                                                    review_user = self.user,
                                                    movie = self.movie,
                                                    rating = 9,
                                                    description="Good Movie",
                                                )
    def test_review_create(self):
        data = {
                "rating": 5,
                "description": "average movie",
                "active": True,
                "review_user": self.user1.id,
                "movie":self.movie.id
            }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.post(reverse('review_list',args=(self.movie.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_review_create_review_twice(self):
        data = {
                "rating": 5,
                "description": "average movie",
                "active": True,
                "review_user": self.user.id,
                "movie":self.movie.id
            }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('review_list',args=(self.movie.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_review_list(self):
        response = self.client.get(reverse('review_list',args=(self.movie.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_get_one(self):
        response = self.client.get(reverse('review_detail',args=(self.movie.id,self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_put(self):
        data = {
                "rating": 1,
                "description": "Tatti movie",
                "active": True,
                "review_user": self.user.id,
                "movie":self.movie.id
            }
        response = self.client.put(reverse('review_detail',args=(self.movie.id,self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_review_delete(self):
        response = self.client.delete(reverse('review_detail',args=(self.movie.id,self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)


class ActorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test",password="Test@1234")
        
        self.token = Token.objects.get(user__username=self.user)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.actor = models.Star.objects.create(full_name='Test Actor',about='This is a test actor description.')

    def test_actor_create(self):
        data = {
                "full_name": "Test",
                "about":"test"
            }

        response = self.client.post(reverse('actor_list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_review_list(self):
        response = self.client.get(reverse('actor_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_get_one(self):
        response = self.client.get(reverse('actor_detail',args=(self.actor.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_put(self):
        data = {
                "full_name": "Test",
                "about":"test"
            }

        response = self.client.put(reverse('actor_detail',args=(self.actor.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_review_delete(self):
        response = self.client.delete(reverse('actor_detail',args=(self.actor.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
