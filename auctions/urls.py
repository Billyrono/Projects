app_name = "auctions"

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="create listing"),
    path("listing/<int:listing_id>", views.listing_page, name="listing page"),
    path("watchlist", views.watchlist_page, name="watchlist page"),
    path("watchlist/toggle/<int:listing_id>", views.watchlist_toggle, name="watchlist toggle"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close auction"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("category", views.category_page, name="category page"),
    path("category/<str:category_name>", views.category_listings, name="category listings")
]
 