from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("watchlist/<int:listing_id>/", views.watchlist_toggle, name="watchlist_toggle"),
    path("bid/<int:listing_id>/", views.bid, name="bid"),
    path("comment/<int:listing_id>/", views.comment, name="comment"),
    path("close_listing/<int:listing_id>/", views.close_listing, name="close_listing"),
    path("won_auctions/", views.won_auctions, name="won_auctions"),
]
