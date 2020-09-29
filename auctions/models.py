from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64, null=False, blank=False)
    category_img = models.CharField(max_length=1400, null=True, blank=True)

    def __str__(self):
        return f"Category: {self.category}"


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    buyer = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="bid_listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=140)
    initial_bid = models.DecimalField(max_digits=20, decimal_places=2)
    current_bid = models.DecimalField(max_digits=20, decimal_places=2)
    image_url = models.CharField(max_length=1400)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name="products")
    active = models.BooleanField(default=True)
    date_posted = models.DateTimeField(auto_now_add=True, editable=False)
    watching = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}: {self.current_bid}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=20, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid of {self.bid} in {self.product.title} by {self.bidder.username}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=140)
    date = models.DateTimeField(auto_now_add=True)
