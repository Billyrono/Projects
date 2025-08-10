# auctions/context_processors.py
# This file was courtesy of chatgpt and is used to add context processors for the auctions app.

def watchlist_count(request):
    if request.user.is_authenticated:
        return {"watchlist_count": request.user.watchlist.count()}
    return {"watchlist_count": 0}
