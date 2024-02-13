from django.db import models
from user.models import User

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.email
    
class Category(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    total_score=models.IntegerField(default=0)
    voters=models.ManyToManyField(User, blank=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self) -> str: 
        return self.title
    
class CategoryItem(models.Model):
    title=models.CharField(max_length=200)
    total_score=models.IntegerField(default=0)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    voters=models.ManyToManyField(User, blank=True)
    manifesto=models.TextField(max_length=500, null=True)


    @property
    def percentage_vote(self):
        category_votes=self.category.total_score
        item_votes= self.total_score

        if category_votes == 0:
            vote_in_percentage=0

        else:
            vote_in_percentage=(item_votes/category_votes) * 100
        return vote_in_percentage

    def __str__(self) -> str:
        return self.title
