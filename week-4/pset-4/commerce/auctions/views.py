from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Auction, Comment

# Index page showing active listings
def index(request):
    listings = Auction.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

# Login view
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

# Logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Registration view
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# Create auction listing view
@login_required
def create(request):
    if request.method == "POST":
        # Get form data
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['starting_bid']
        image_url = request.POST['image_url']
        category = request.POST['category']
        
        # Create a new Auction listing
        auction = Auction(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_bid=starting_bid,  # Set the initial bid to starting_bid
            image_url=image_url,
            category=category,
            created_by=request.user  # Associate the listing with the current user
        )
        auction.save()
        
        # Redirect to the index page or the listing page
        return redirect('index')

    # Render the empty form on GET request
    return render(request, "auctions/create.html")

# Listing detail view (showing comments and bids)
def listing(request, listing_id):
    listing = get_object_or_404(Auction, pk=listing_id)
    comments = listing.listing_comments.all()  # Fetch all related comments
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
    })

# Toggle watchlist view
@login_required
def watchlist_toggle(request, listing_id):
    listing = get_object_or_404(Auction, pk=listing_id)
    
    # Check if the listing is already in the user's watchlist
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)  # Remove from watchlist
    else:
        request.user.watchlist.add(listing)  # Add to watchlist
    
    return redirect('listing', listing_id=listing_id)

# Bid on listing view
@login_required
def bid(request, listing_id):
    listing = get_object_or_404(Auction, pk=listing_id)

    if request.method == "POST":
        bid_amount = float(request.POST['bid'])

        # Check if the bid is greater than the current bid
        if bid_amount > listing.current_bid:
            listing.current_bid = bid_amount
            listing.save()
            # Redirect to the listing page
            return redirect('listing', listing_id=listing_id)
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "error": "Your bid must be higher than the current bid.",
                "comments": listing.listing_comments.all()  # Ensure comments are still shown
            })

    return redirect('listing', listing_id=listing_id)

# Comment on listing view
@login_required
def comment(request, listing_id):
    listing = get_object_or_404(Auction, pk=listing_id)

    if request.method == "POST":
        comment_text = request.POST['comment']
        
        # Create a new comment
        new_comment = Comment(
            user=request.user,
            text=comment_text,
            listing=listing
        )
        new_comment.save()
        
        # Redirect back to the listing page
        return redirect('listing', listing_id=listing_id)
    
    return redirect('listing', listing_id=listing_id)

# Close auction listing view
@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Auction, pk=listing_id)

    # Only the user who created the listing can close it
    if request.user == listing.created_by:
        # Mark the listing as closed
        listing.is_active = False

        # Find the highest bid
        highest_bid = listing.bid_set.order_by('-bid_amount').first()

        # Assign the winner if there was a bid
        if highest_bid:
            listing.winner = highest_bid.user

        listing.save()

    return redirect('listing', listing_id=listing_id)

@login_required
def won_auctions(request):
    won_auctions = request.user.won_auctions.all()  # Get all auctions the user has won
    return render(request, "auctions/won_auctions.html", {
        "won_auctions": won_auctions
    })
