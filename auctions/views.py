from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User
from django import forms
from .models import AuctionListing, Bid, Comment, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify

class NewAuctionForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = [
            'title',
            'description',
            'estimated_price_min',
            'estimated_price_max',
            'starting_bid_price',
            'image_url',
            'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter listing title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your item',
                'rows': 4
            }),
            'estimated_price_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minimum estimated price'
            }),
            'estimated_price_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maximum estimated price'
            }),
            'starting_bid_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Starting bid price'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Image URL'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        username = f"{first_name} {last_name}"
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def listing_page(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)

    is_winner = request.user == listing.auction_winner if not listing.is_active else False

    return render(request, "auctions/listing.html",{
      "listing": listing,
      "is_winner": is_winner,
      "comments": listing.comments.all()
    })

def category_slugify(name):
    slug = slugify(name)
    slug = slug.replace("-and-", "-").replace("-&-", "-")
    return slug

def category_page(request):
    categories = Category.objects.all()
 
    categories_slugs = [
        {
            "name": category.name,
            "slug": category_slugify(category.name)
        }
        for category in categories
    ]

    return render(request, "auctions/categories.html", {
        "categories": categories_slugs
    })


def category_listings(request, category_name):
    category = Category.objects.get(name=category_name)
    listings = AuctionListing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

@login_required(login_url="auctions:login")
def new_listing(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST)

        if form.is_valid():
            auction = form.save(commit=False)
            auction.created_by = request.user
            auction.save() 
            return redirect("auctions:index")
        
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
        
    form = NewAuctionForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

@login_required(login_url="auctions:login")
def watchlist_page(request):
    user = request.user
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required(login_url="auctions:login")
def watchlist_toggle(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    user = request.user
    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    return redirect("auctions:watchlist page")

@login_required(login_url="auctions:login")
def bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    user = request.user

    highest_bid = listing.bids.order_by('-amount_bid').first()
    current_price = highest_bid.amount_bid if highest_bid else listing.starting_bid_price

    if request.method == "POST":
        try:
            amount_bid = float(request.POST.get("bid"))
            
            if amount_bid <= current_price:
                messages.error(request, "Your bid must be greater than the current bid.")
            else:
                new_bid = Bid(user=user, auction_listing=listing, amount_bid=amount_bid)
                new_bid.save()
                listing.starting_bid_price = amount_bid
                listing.save()
                messages.success(request, "Your bid was successfully placed!")
                
                return redirect("auctions:listing page", listing_id=listing_id)
        except (ValueError, TypeError):
            messages.error(request, "Invalid bid amount.")
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": listing.starting_bid_price,
        "highest_bid": highest_bid,
    })

@login_required(login_url="auctions:login")
def close_auction (request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    
    if request.method == "POST":
        listing.is_active = False
        highest_bid = listing.bids.order_by('-amount_bid').first()
        if highest_bid:
            listing.auction_winner = highest_bid.user
            listing.save()
            messages.success(request, "Auction closed successfully.")
            
            return redirect("auctions:listing page", listing_id=listing_id)

@login_required(login_url="auctions:login")
def comment(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    user = request.user

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            comment = Comment(user=user, auction_listing=listing, text= text)
            comment.save()

            return redirect("auctions:listing page", listing_id=listing_id)
    
   