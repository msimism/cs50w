from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Auction, Comment, Bid, User

# Register the Auction model
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'starting_bid', 'current_bid', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'description', 'created_by__username')

# Register the Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'text', 'created_at')
    search_fields = ('user__username', 'listing__title', 'text')

# Register the Bid model
class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'bid_amount', 'created_at')
    search_fields = ('user__username', 'listing__title', 'bid_amount')

# Register the models in the admin panel
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(User, UserAdmin)
