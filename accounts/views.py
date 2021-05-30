import random

from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.models import UserCreateForm
from app.models import Profile


def sign_up(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save()
            btc_balance = round(random.uniform(0.00, 10.00), 2)
            usd_balance = round(random.uniform(0.00, 1000000.00), 2)
            Profile.objects.create(user=user, btc_balance=btc_balance, usd_balance=usd_balance)

            messages.success(request, f'Account created, you got {btc_balance} BTC and {usd_balance} USD')
            return redirect('/accounts/login')
    else:
        form = UserCreateForm

    return render(request, 'accounts/sign_up.html', {'form': form})

