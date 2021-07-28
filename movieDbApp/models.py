from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

class StreamingPlatform(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    about = models.CharField(_("About"), max_length=255)
    website = models.URLField(_("Website"), max_length=200)
    

    class Meta:
        verbose_name = _("StreamingPlatform")
        verbose_name_plural = _("StreamingPlatforms")
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("StreamingPlatform_detail", kwargs={"pk": self.pk})


class Movie(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    description = models.CharField(_("Description"), max_length=255)
    platform = models.ForeignKey(StreamingPlatform,on_delete=models.CASCADE,related_name='movies')
    active = models.BooleanField(_("Active"),default=True)
    average_rating = models.FloatField(_("Average Rating"),default=0)
    number_rating = models.IntegerField(_("Total Reviews"),default=0)
    released_on = models.DateTimeField(_("Released On"), auto_now=False, auto_now_add=True)
    

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"pk": self.pk})


class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='review_user')
    rating = models.PositiveSmallIntegerField(_("Rating"),validators=[MinValueValidator(1),MaxValueValidator(10)])
    description = models.CharField(_("Description"), max_length=200,null=True,blank=True)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['id']

    def __str__(self):
        return f"Rating : {self.rating} <<>> Content : {self.description}"

    def get_absolute_url(self):
        return reverse("review_detail", kwargs={"pk": self.pk})
