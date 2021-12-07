# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm


def homepage(request):
    """
    Show the number of different orders and the details
    """
    order = Order.objects.all()
    order_count = order.count()

    order_p_count = Order.objects.filter(status='pending').count()
    order_c_count = Order.objects.filter(status='confirmed').count()

    if request.is_ajax and request.POST.get('order_del'):
        del_order_id = request.POST.get('order_del')
        del_order = Order.objects.get(id = del_order_id)
        del_order.delete()

    context = {
        'order_count': order_count,
        'order_p_count': order_p_count,
        'order_c_count': order_c_count,
        'order': order,
    }
    
    return render(request, 'OrderConfirm/home.html', context)


def update_order(request, pk):
    """
    Post whether to change the status of the order
    """
    order = Order.objects.get(id=pk)
    order_form = OrderForm(instance=order)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            Dno_get = order_form.cleaned_data['Dno']
            Dvalue_get = order_form.cleaned_data['Dvalue']
            Tno_get = order_form.cleaned_data['Tno']
            Sno_get = order_form.cleaned_data['Sno']
            status_get = order_form.cleaned_data['status']
            order = Order.objects.filter(id=pk)
            order.update(id=pk, Dno=Dno_get, Dvalue=Dvalue_get, Tno=Tno_get, Sno=Sno_get, status=status_get)
            return redirect('orderconfirm')

    context = {
        'order': order,
        'order_form': order_form
    }
    return render(request, 'OrderConfirm/updateorder.html', context)


def delete_order(request, pk):
    """
    Post whether to delete the order
    """
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('orderconfirm')

    context = {
        'order': order,
    }
    return render(request, 'OrderConfirm/deleteorder.html', context)
