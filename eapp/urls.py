from django.urls import path, include
from eapp.views import HomeView, ItemDetailView, OrderSummaryView
from eapp import views

app_name = 'eapp'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('Order_Summary_View/', OrderSummaryView.as_view(), name='Order_Summary'),
    path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/', views.remove_single_item_from_cart,
         name='remove_single_item_from_cart'),
    path('add_single_item_from_cart/<slug>/', views.add_single_item_from_cart,
         name='add_single_item_from_cart'),
]
