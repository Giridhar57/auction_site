from django.shortcuts import render, redirect
from rest_framework import generics
from django.utils import timezone
from datetime import datetime
from .forms import AuctionCreationForm, BidForm
from .models import Auction,Bid
from user_management.models import CustomUser
from .serializers import AuctionSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from user_management.views import logout,login
from django.http import HttpResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
import requests




class AuctionListView(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    template_name = 'auction_list.html'
    context_object_name = 'auctions'

class AuctionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    template_name = 'auction_detail.html'
    context_object_name = 'auction'

def highest_bidder(auction_id):
    highest_bid=Bid.objects.filter(auction=auction_id).order_by("-amount")
    if(highest_bid):
        return highest_bid[0]
    return None

# http http://127.0.0.1:8000/auctions/my_bids "Authorization: Token 55a560e616f80ce393212abae3b20ff15b6cd398"

def get_user(token):
    user=None
    if token:
        for user in CustomUser.objects.all():
            if(user.auth_token==token):
                user=user
    return user

def home(requests):
    return render(requests,"home.html")


@login_required
def auction_list(request):
    user=request.user
    print(settings.API_SECRET)
    print(user)
    auctions = Auction.objects.all()
    for auction in auctions:
        if(auction.start_time<datetime.now() and auction.end_time>=datetime.now()):
            auction.status="Live Now"
        elif(auction.start_time>datetime.now()):
            auction.status="Not Yet Started"
        else:
            highest_bid=Bid.objects.filter(auction=auction.id).order_by("-amount")
            if(highest_bid):
                auction.winner=highest_bid[0].user
                auction.save()
            auction.status="Auction Completed"
    return render(request, 'auction_list.html', {'auctions': auctions,'user':user})

@login_required
def auction_detail(request,pk):
    auction = get_object_or_404(Auction, pk=pk)
    print(request.user)
    if(auction.start_time<datetime.now() and auction.end_time>=datetime.now()):
        auction.live=True
    # serializer = AuctionSerializer(auction)
    # print(serializer.data)
    bidded_value=None
    if(Bid.objects.filter(auction_id=auction.id).filter(user_id=request.user.id)):
        bidded_value=Bid.objects.filter(auction_id=auction.id).filter(user_id=request.user.id)[0]
    return render(request, 'auction_detail.html', {'auction': auction,'highest_bidder':highest_bidder(auction.id),'bidded_value':bidded_value})

@login_required
def auction_create(request):
    print(request.user)
    if(request.user.is_superuser):
        if request.method == 'POST':
            form = AuctionCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('auction_list')  # Assuming you have a auction list view named 'auction-list'
        else:
            form = AuctionCreationForm()

        return render(request, 'auction_create.html', {'form': form})
    return HttpResponse("<h1 style='color:red;'>Action Not Allowed</h1>")

@login_required
def auction_delete(request,pk):
    if(request.user.is_superuser):
        auction = get_object_or_404(Auction, pk=pk)
        auction.delete()
        return redirect("auction_list")
    return HttpResponse("<h1 style='color:red;'>Action Not Allowed</h1>")

@login_required
def auction_edit(request,pk):
    if(request.user.is_superuser):
        auction=get_object_or_404(Auction, pk=pk)
        if request.method == 'POST':
            form = AuctionCreationForm(request.POST, instance=auction)
            if form.is_valid():
                if(form.cleaned_data['end_time']>=datetime.now()):
                    auction.winner=None
                elif(form.cleaned_data['end_time']<datetime.now()):
                    highest_bid=Bid.objects.filter(auction=auction.id).order_by("-amount")
                    if(highest_bid):
                        print(highest_bid[0].user)
                        auction.winner=highest_bid[0].user
                auction.save()
                form.save()
                return redirect('auction_detail', pk=pk)
        else:
            form = AuctionCreationForm()
        return render(request,'auction_edit.html',{'auction':auction,'form':form})
    return HttpResponse("<h1 style='color:red;'>Action Not Allowed</h1>")

@login_required
def bid_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    form = BidForm(request.POST or None)
    if(auction.start_time<datetime.now() and auction.end_time<datetime.now()):
        return HttpResponse("<h1 style='color:red'>Bidding Time Out!! Action not allowed!!</h1>")
    if(auction.start_time>datetime.now()):
        return HttpResponse("<h1 style='color:red'>Bidding Yet to Start!! Action not allowed!!</h1>")
    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        bid = Bid.objects.create(auction=auction, user=request.user, amount=amount)
        # if(auction.highest_bid and auction.highest_bid<bid.amount):
        #     auction.highest_bid = bid.amount
        #     auction.save()
        return redirect('auction_detail', pk=pk)
    
    return render(request, 'bid_auction.html', {'auction': auction, 'form': form})
@login_required
def bid_edit(request, pk):
    bid = Bid.objects.filter(auction_id=pk).filter(user_id=request.user.id)[0]
    auction=get_object_or_404(Auction,pk=pk)
    if(auction.start_time<datetime.now() and auction.end_time<datetime.now()):
        return HttpResponse("<h1 style='color:red'>Bidding Time Out!! Action not allowed!!</h1>")
    if(auction.start_time>datetime.now()):
        return HttpResponse("<h1 style='color:red'>Bidding Yet to Start!! Action not allowed!!</h1>")
    form = BidForm(request.POST or None)
    if(bid.auction.end_time<datetime.now()):
        return HttpResponse("<h1 style='color:red'>Bidding Time Out!! Action not allowed!!</h1>")
    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']
        bid.amount=amount
        bid.save()
        # if(auction.highest_bid and auction.highest_bid<bid.amount):
        #     auction.highest_bid = bid.amount
        #     auction.save()
        return redirect('auction_detail', pk=pk)
    
    return render(request, 'bid_auction.html', {'auction': auction, 'form': form,'bid':bid})

@login_required
def view_bids(request, auction_id):
    bids = Bid.objects.filter(auction_id=auction_id)
    auction=get_object_or_404(Auction, pk=auction_id)
    return render(request,'view_bids.html',{'bids':bids,'auction':auction})

@login_required
def my_bids(request):
    user=request.user
    token=request.META.get('HTTP_AUTHORIZATION')
    if token:
        user=get_user(token)
    bids = Bid.objects.filter(user=user.id)
    return render(request,'my_bids.html',{'bids':bids})


@authentication_classes('rest_framework.authentication.TokenAuthentication')
@permission_classes('IsAuthenticated')
@api_view(('GET',))
def all_auctions(requests):
    data_live=Auction.objects.filter(start_time__lt=datetime.now(),end_time__gte=datetime.now())
    data_completed=Auction.objects.filter(start_time__lt=datetime.now(),end_time__lt=datetime.now())
    data_upcoming=Auction.objects.filter(start_time__gt=datetime.now())
    serializer_live=AuctionSerializer(data_live,many=True)
    serializer_completed=AuctionSerializer(data_completed,many=True)
    serializer_upcoming=AuctionSerializer(data_upcoming,many=True)
    response = {
                   "status": status.HTTP_200_OK,
                   "message": "success",
                   "data": {"live":[serializer_live.data],"completed":[serializer_completed.data],"upcoming":[serializer_upcoming.data]}
                }
    return Response(response, status = status.HTTP_200_OK)


@authentication_classes('rest_framework.authentication.TokenAuthentication')
@permission_classes('IsAuthenticated')
@api_view(('GET',))
def my_biddings(request):
    data=[]
    token=request.META.get('HTTP_AUTHORIZATION')
    user=get_user(token)
    bids=Bid.objects.filter(user_id=user)
    for bid in bids:
        temp={}
        temp['id']=bid.id
        temp['auction_id']=bid.auction.id
        temp['base_price']=bid.auction.start_price
        temp['item_name']=bid.auction.item_name
        temp['amount']=bid.amount
        x=Bid.objects.filter(auction=bid.auction.id).order_by("-amount")
        if(x):
            temp['higest_bid_amount']=x[0].amount
        if(bid.auction.winner):
            if(bid.auction.winner==user):
                temp['status']="You won this Auction"
            else:
                temp['status']="Lost"
        else:
            temp['status']="Ongoing"
        data.append(temp)
    response = {
                   "status": status.HTTP_200_OK,
                   "message": "success",
                   "data": data
                }
    return Response(response, status = status.HTTP_200_OK)

@authentication_classes('rest_framework.authentication.TokenAuthentication')
@permission_classes('IsAuthenticated')
@api_view(('GET',))
def auction_bid(request, pk,amount):
    auction = get_object_or_404(Auction, pk=pk)
    token=request.META.get('HTTP_AUTHORIZATION')
    if(auction.start_price>amount):
        return Response({f"Amount Must be higher than base price({auction.start_price})"}, status = status.HTTP_200_OK)
    user=get_user(token)
    if(auction.start_time<datetime.now() and auction.end_time<datetime.now()):
        return HttpResponse("<h1 style='color:red'>Bidding Time Out!! Action not allowed!!</h1>")
    if(auction.start_time>datetime.now()):
        return HttpResponse("<h1 style='color:red'>Bidding Yet to Start!! Action not allowed!!</h1>")
    try:
        bid=Bid.objects.get(auction_id=pk,user=user)
        bid.amount=amount
        bid.save()
    except:
        bid = Bid.objects.create(auction=auction, user=user, amount=amount)
    data=[]
    data.append({'bid_id':bid.id,'quoted_amount':bid.amount,'item_name':bid.auction.item_name,'base_amount':bid.auction.start_price,'auction_id':bid.auction.id})
    response = {
                   "status": status.HTTP_200_OK,
                   "message": "success",
                   "data": data
                }
    return Response(response, status = status.HTTP_200_OK)

