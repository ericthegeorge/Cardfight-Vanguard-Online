from django.contrib import admin
from .models import Card, UserProfile, UserDeck, DeckCard
# Register your models here.

# admin.site.register(Cards)
# admin.site.register(UserProfile)

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity')  # Show these fields in the admin list view
    search_fields = ('name',)         # Add a search bar for the 'name' field
    list_filter = ('rarity',)         # Add filters for the 'rarity' field

class CardInline(admin.TabularInline):
    model = UserProfile.cards.through  # Access the many-to-many intermediate table
    extra = 1                          # Number of blank card slots shown

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [CardInline]

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(UserDeck)
admin.site.register(DeckCard)
