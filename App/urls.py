from django.urls import path
from .views import (
    browse, buy, item, home, portfolio, settings,
    watchlist, trending
)

urlpatterns = [
    path('', home.home, name='home'),
    path('browse/', browse.browse, name='browse'),
    path('buy/', buy.buy, name='buy'),
    path('item/<str:item_id>', item.item, name='item'),
    path('portfolio/', portfolio.portfolio, name='portfolio'),
    path('settings/', settings.settings, name='settings'),
    path('watchlist/', watchlist.watchlist, name='watchlist'),
    path('trending/', trending.trending, name='trending'),
]