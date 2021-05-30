from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from app.forms import OrderForm
from app.models import Profile, Order
from app.utils import BitcoinInfo


@login_required
def index(request):

    btc_info = BitcoinInfo()
    btc_price = round(btc_info.get_price(), 2)

    user_profile = Profile.objects.filter(user=request.user)[0]

    if request.method == "POST":
        form = OrderForm(request.POST, request=request)

        if form.is_valid():

            order = form.save(commit=False)
            order.quantity_left = order.quantity
            user_profile = Profile.objects.filter(user=request.user)[0]
            order.profile = user_profile

            if order.order_type == "Buy":
                sell_orders = Order.objects.filter(order_type='Sell').filter(status='Pending').filter(
                    ~Q(profile=user_profile)).filter(price__lte=order.price).order_by('-price')

                for sell_order in sell_orders:

                    if order.quantity_left > sell_order.quantity_left:
                        sell_order.status = 'Completed'

                        sell_order.profile.btc_balance -= sell_order.quantity
                        sell_order.profile.usd_balance += (sell_order.quantity * sell_order.price)
                        sell_order.profile.profit += (sell_order.quantity * sell_order.price)

                        order.quantity_left -= sell_order.quantity_left

                        sell_order.quantity_left = 0
                        sell_order.profile.save()
                        sell_order.save()

                        order.profile.save()
                        order.save()

                    elif order.quantity_left == sell_order.quantity_left:
                        sell_order.status = 'Completed'
                        order.status = 'Completed'

                        sell_order.profile.btc_balance -= sell_order.quantity
                        sell_order.profile.usd_balance += (sell_order.quantity * sell_order.price)
                        sell_order.profile.profit += (sell_order.quantity * sell_order.price)

                        order.profile.btc_balance = order.profile.btc_balance + order.quantity
                        order.profile.usd_balance -= (order.quantity * order.price)
                        order.profile.profit -= (order.quantity * order.price)

                        sell_order.quantity_left = 0
                        sell_order.profile.save()
                        sell_order.save()

                        order.quantity_left = 0
                        order.profile.save()
                        order.save()

                    elif order.quantity_left < sell_order.quantity_left:
                        order.status = 'Completed'

                        order.profile.btc_balance = order.profile.btc_balance + order.quantity
                        order.profile.usd_balance -= (order.quantity * order.price)
                        order.profile.profit -= (order.quantity * order.price)

                        sell_order.quantity_left -= order.quantity_left
                        sell_order.profile.save()
                        sell_order.save()

                        order.quantity_left = 0
                        order.profile.save()
                        order.save()

                        break

            elif order.order_type == "Sell":
                buy_orders = Order.objects.filter(order_type='Buy').filter(status='Pending').filter(
                    ~Q(profile=user_profile)).filter(price__gte=order.price).order_by('price')

                for buy_order in buy_orders:

                    if order.quantity_left > buy_order.quantity_left:
                        buy_order.status = 'Completed'

                        buy_order.profile.btc_balance += buy_order.quantity
                        buy_order.profile.usd_balance -= (buy_order.quantity * buy_order.price)
                        buy_order.profile.profit -= (buy_order.quantity * buy_order.price)

                        order.quantity_left -= buy_order.quantity_left

                        buy_order.quantity_left = 0
                        buy_order.profile.save()
                        buy_order.save()

                        order.profile.save()
                        order.save()

                    elif order.quantity_left == buy_order.quantity_left:
                        buy_order.status = 'Completed'
                        order.status = 'Completed'

                        buy_order.profile.btc_balance += buy_order.quantity
                        buy_order.profile.usd_balance -= (buy_order.quantity * buy_order.price)
                        buy_order.profile.profit -= (buy_order.quantity * buy_order.price)

                        order.profile.btc_balance -= order.quantity
                        order.profile.usd_balance += (order.quantity * order.price)
                        order.profile.profit += (order.quantity * order.price)

                        buy_order.quantity_left = 0
                        buy_order.profile.save()
                        buy_order.save()

                        order.quantity_left = 0
                        order.profile.save()
                        order.save()

                    elif order.quantity_left < buy_order.quantity_left:
                        order.status = 'Completed'

                        order.profile.btc_balance -= order.quantity
                        order.profile.usd_balance += (order.quantity * order.price)
                        order.profile.profit += (order.quantity * order.price)

                        buy_order.quantity_left -= order.quantity_left
                        buy_order.profile.save()
                        buy_order.save()

                        order.quantity_left = 0
                        order.profile.save()
                        order.save()
                        break

            order.profile.save()
            order.save()
            messages.success(request, f'Order created, check your orders history')

            return redirect('/')
    else:
        form = OrderForm(request=request)

    btc_to_usd = int(user_profile.btc_balance * btc_price)
    total_balance_usd = user_profile.usd_balance + btc_to_usd
    btc_perc = int((btc_to_usd / total_balance_usd) * 100)
    usd_perc = 100 - btc_perc

    user_info = {
        'btc_balance': user_profile.btc_balance,
        'usd_balance': user_profile.usd_balance,
        'usd_perc': usd_perc,
        'btc_perc': btc_perc,
        'btc_to_usd': btc_to_usd
    }

    user_orders = Order.objects.filter(profile=user_profile).order_by('-datetime')

    context = {
        'user_info': user_info,
        'user_orders': user_orders
    }
    return render(request, 'app/index.html', {'form': form, 'context': context})
