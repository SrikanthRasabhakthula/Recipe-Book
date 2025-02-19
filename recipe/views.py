from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'home.html')


@login_required(login_url='login')
def add(request):
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        description = data.get("description")
        image = request.FILES.get("image")
        
        Recipe.objects.create(name=name,description=description,image=image)
        return redirect("show")
    return render(request,'add.html')



@login_required(login_url='login')
def show(request):
    queryset = Recipe.objects.all()
    if request.GET.get('search'):
        queryset=queryset.filter(name__icontains = request.GET.get('search'))
    return render(request,'show.html',{'recipes':queryset})


@login_required
def detail(request,id):
    queryset=Recipe.objects.get(id=id)
    return render(request,"details.html",{'recipe':queryset})

@login_required(login_url='login')
def delete(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('show')


@login_required(login_url='login')
def update(request,id):
    queryset = Recipe.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        description = data.get("description")
        image = request.FILES.get("image")

        queryset.name=name
        queryset.description=description
        if image:
            queryset.image =image
        queryset.save()
        return redirect('show')
    return render(request,"update.html",{'recipe':queryset})


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return render(request, 'login.html')
        
        user = authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,'Invalid Username')
            return render(request, 'login.html')
        else:
            login(request,user)
            return render(request, "home.html")
        
    return render(request,'login.html')


def logout_page(request):
    logout(request)
    
    return redirect('login')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'User already taken')
            return redirect('register')
            
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=make_password(password) 
        )
        if user:
            messages.success(request,'Successfully Registered')
        return redirect('register') 

    return render(request, 'register.html')
