from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
    
class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    estimated_price_min = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_price_max = models.DecimalField(max_digits=10, decimal_places=2)
    starting_bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    auction_winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won")

    def __str__(self):
        return f"{self.title} - ${self.starting_bid_price}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    amount_bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount_bid} on {self.auction_listing.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.text} on {self.auction_listing.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"