import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from movieDbApp import models

class Command(BaseCommand):
    help = 'Generate Random Test DataSet.'

    def handle(self, *args, **kwargs):
        # creating users 100 users
        print("DataSet Generation started...\n\nCreating users...\n")
        for i in range(100):
            u  = User.objects.create_user(username=f"user{i+1}",email=f"user{1}@gmail.com",password="User@1234")

        print("\nCreating Streaming Platforms...")
        platforms = [
                {
                    "name": "NetFlix",
                    "about": "#1 Streaming Platform",
                    "website": "https://netflix.com"
                },
                {
                    "name": "PrimeVideos",
                    "about": "Amazon Prime Videos",
                    "website": "http://primevideos.com"
                },
                {
                    "name": "Disny+Hotstar",
                    "about": "Hotstar an disny plus",
                    "website": "http://hotstar.in"
                },
                {
                    "name": "HBO",
                    "about": "HBO entertainments",
                    "website": "http://hbo.com"
                }
        ]

        for i in platforms:
            p = models.StreamingPlatform.objects.create(name=i.get('name'),about=i.get('about'),website=i.get('website'))
            p.save()

        print("\nCreating Stars ...")
        for i in range(100):
            a = models.Star.objects.create(full_name=f"Actor{i+1}",about=f"Lorem Ipsum is simply dummy text of the printing and typesetting industry.{i+1}")
            a.save()

        print("\nCreating Movies ...")
        s = models.StreamingPlatform.objects.all()
        a = models.Star.objects.all()
        for i in range(500):
            x = [random.choice(a) for i in range(random.randint(4,10))]
            m = models.Movie(name=f"Movie {i+1}",description=f"Description {i+1}",platform=random.choice(s))
            m.save()
            m.stars.set(x)
            m.save()
        
        print("\nGenerating Reviews ...")
        review = ['Good Movie','Excellent','Very Very Good Movie','Worst Movie']
        LIMIT = 1500
        count = 0
        limit_reached = False
        for u in User.objects.all():
            for m in models.Movie.objects.all():
                r = models.Review.objects.create(review_user=u,movie=m,rating=random.randint(1,10),description=random.choice(review))
                r.save()
                if count==LIMIT:
                    limit_reached=True
                    break
                count+=1
            if limit_reached:
                break


        print("\n********** Data Generating Completed **********")
        
        

