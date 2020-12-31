from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
from django.utils import timezone

from django.contrib import messages

# Create your views here.


def checkout(request):
    return render(request, 'checkout.html')


class HomeView(ListView):
    model = Item
    template_name = 'home.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    # checking user no order che ke nahi..
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # jo item ma order hase to...
    if order_qs.exists():
        order = order_qs[0]

        # check if the order item is in the order
        # means jo item already hase to...
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was updated.')

        else:
            messages.info(request, 'This item was add to your cart.')
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This item was add to your cart.')

    return redirect("eapp:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        # check if the order item is in the order
        # means jo item already hase to...
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            order.delete()
            messages.info(request, 'This item was remove from your cart.')

        else:
            messages.info(request, 'This item was not in your cart.')
            return redirect("eapp:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("eapp:product", slug=slug)

    return redirect("eapp:product", slug=slug)
