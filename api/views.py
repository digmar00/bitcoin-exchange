from django.http import JsonResponse
from django.shortcuts import render

from app.models import Order, Profile


def api(request):
    return render(request, 'api/api.html')


def get_orders(request):
    order_status = request.GET.get('status')
    order_type = request.GET.get('type')

    orders_info = []

    if order_status is not None and order_type is not None:
        orders = Order.objects.filter(order_type='Buy').filter(status='Pending')
    elif order_status is not None:
        orders = Order.objects.filter(status=order_status)
    elif order_type is not None:
        orders = Order.objects.filter(order_type=order_type)
    else:
        orders = Order.objects.filter()

    for order in orders:
        orders_info.append(
            {
                'username': order.profile.user.username,
                'datetime': order.datetime,
                'price': order.price,
                'quantity': order.quantity,
                'type': order.order_type,
                'status': order.status
            }
        )

    return JsonResponse(orders_info, safe=False)


def get_profiles(request):
    profiles_info = []

    profiles = Profile.objects.filter()

    for profile in profiles:
        profiles_info.append(
            {
                'username': profile.user.username,
                'btc_balance': profile.btc_balance,
                'usd_balance': profile.usd_balance,
                'profit': profile.profit
            }
        )

    return JsonResponse(profiles_info, safe=False)
