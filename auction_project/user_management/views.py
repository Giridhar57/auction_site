from django.shortcuts import render, redirect
from rest_framework import generics
from .forms import CustomUserCreationForm
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth import login, authenticate,logout
from auction_management.views import auction_list
from rest_framework.authtoken.models import Token
import requests
from django.urls import reverse
from django.http import HttpResponse


class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

def all_users(requests):
    if(requests.user.is_superuser):
        users=CustomUser.objects.all()
        return render(requests,'all_users.html',{'users':users})
    return HttpResponse("<h1 style='color:red'>Not Allowed!!!!!</h1>")

def view_user(requests,pk):
    if(requests.user.is_superuser):
        user=CustomUser.objects.get(pk=pk)
        token, created = Token.objects.get_or_create(user=user)
        return render(requests,'view_user.html',{"user":user,"token":token.key})
    return HttpResponse("<h1 style='color:red'>Not Allowed!!!!!</h1>")

def delete_user(requests,pk):
    if(requests.user.is_superuser):
        user=CustomUser.objects.get(pk=pk)
        user.delete()
        return redirect("all_users")
    return HttpResponse("<h1 style='color:red'>Not Allowed!!!!!</h1>")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password1']
            form.save()
            user = authenticate(request,username=username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            print("token:",token)
            if user is not None:
                login(request, user)
                return redirect("auction_list")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            # headers={}
            # headers['Authorization'] = f'Token {token.key}'
            # x=requests.get(f"http://127.0.0.1:8000{reverse('auction_list')}",headers=headers)
            # return HttpResponse(x.text)
            return redirect("auction_list")  # Assuming you have a auction list view named 'auction_list'
        else:
            return redirect("login")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

