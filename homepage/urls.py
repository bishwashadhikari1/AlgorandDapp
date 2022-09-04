from django.urls import path
from . import views

urlpatterns =  [ 
 path ('', views.home_index, name='home'),
 path ('createwallet/', views.create_wallet, name='createwallet'),
 path ('confirmcreation/', views.confirm_creation, name='confirm_creation'),
 path ('wallethome/', views.wallet_home, name='wallethome'),
 path ('importwallet/', views.import_wallet, name='importwallet'),



]