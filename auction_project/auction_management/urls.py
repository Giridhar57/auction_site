from django.urls import path
from .views import AuctionListView, AuctionDetailView
from . import views
from user_management.views import user_login

urlpatterns = [
    # path('auctions/', AuctionListView.as_view(), name='auction-list'),
    path('auctions/',views.home,name="home"),
    path('accounts/login/',user_login,name="login"),
    path('auctions/list',views.auction_list,name='auction_list'),
    path('auctions/<int:pk>',views.auction_detail,name='auction_detail'),
    # path('auctions/<int:pk>/', AuctionDetailView.as_view(), name='auction-detail'),
    path('auctions/create', views.auction_create, name='auction_create'),
    path('auctions/delete/<int:pk>', views.auction_delete, name='auction_delete'),
    path('auctions/edit/<int:pk>', views.auction_edit, name='auction_edit'),
    path('auctions/bid/<int:pk>',views.bid_auction,name="bid_auction"),
    path('auctions/bid/edit/<int:pk>',views.bid_edit,name="bid_edit"),
    path('auctions/view_bids/<int:auction_id>',views.view_bids,name="view_bids"),
    path('auctions/my_bids',views.my_bids,name="my_bids"),
    path('all_auctions',views.all_auctions,name='all_auctions'),
    path('my_biddings',views.my_biddings,name='my_biddings'),
    path('auction_bid/<int:pk>/<int:amount>',views.auction_bid,name='auction_bid'),
]