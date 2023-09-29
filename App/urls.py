from django.urls import path
from .views import (
    browse, buy, item, home, portfolio, settings,
    watchlist, trending, login, sign_up, portfolio_item
)
from .views.redirects import (
    add_to_watchlist, logout, pages,
    item_type_filter, metric_filter, winners_losers_filter,
    graph_range, update_portfolio_item
)

urlpatterns = [
    path('', home.home, name='home'),
    path('browse/', browse.browse, name='browse'),
    path('buy/', buy.buy, name='buy'),
    path('item/<str:item_id>', item.item, name='item'),
    path('portfolio/', portfolio.portfolio, name='portfolio'),
    path('portfolio/<str:item_id>/', portfolio_item.portfolio_item, name='portfolio_item'),
    path('update_portfolio_item/<str:item_id>', update_portfolio_item.update_portfolio_item, name='update_portfolio_item'),
    path('settings/', settings.settings, name='settings'),
    path('watchlist/', watchlist.watchlist, name='watchlist'),
    path('trending/', trending.trending, name='trending'),
    path('add_to_watchlist/<str:item_id>/', add_to_watchlist.add_to_watchlist, name='add_to_watchlist'),
    path('pages/<str:redirect_view>/', pages.pages, name='pages'),
    path('item_type_filter/<str:redirect_view>/', item_type_filter.item_type_filter, name='item_type_filter'),
    path('metric_filter/<str:redirect_view>/', metric_filter.metric_filter, name='metric_filter'),
    path('winners_losers_filter/<str:redirect_view>/', winners_losers_filter.winners_losers_filter, name='winners_losers_filter'),
    path('graph_range/<str:redirect_view>', graph_range.graph_range, name='graph_range'),
    path('login/', login.login, name='login'),
    path('sign_up/', sign_up.sign_up, name='sign_up'),
    path('logout/', logout.logout, name='logout')
]