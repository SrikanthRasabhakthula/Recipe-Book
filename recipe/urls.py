
from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path('add/',add,name='add'),
    path("show/",show,name="show"),
    path("detail/<int:id>/",detail,name="detail"),
    
    path('delete/<int:id>/',delete,name='delete'),
    path('update/<int:id>/',update,name='update'),
    path("login/",login_page,name="login"),
    path('logout',logout_page,name='logout'),
    path("register/",register,name="register"),
]

