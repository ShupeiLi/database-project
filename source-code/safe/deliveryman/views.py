# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .models import Health, Distribution
from .forms import HealthForm, DistributionForm


def health(request):
    """
    Show the health information of the deliveryman
    """
    health = Health.objects.all()

    context = {
        'health': health,
    }
    
    return render(request, 'deliveryman/health.html', context)


def create_health(request):
    """
    Deliveryman create today's health information
    """
    health_form = HealthForm()

    if request.method == 'POST':
        if 'c-button' in request.POST:
            health_form = HealthForm(request.POST)
            if health_form.is_valid():
                username_get = health_form.cleaned_data['username']
                pcity_get = health_form.cleaned_data['pcity']
                ptemp_get = health_form.cleaned_data['ptemp']
                health = Health.objects.create(username=username_get, pcity=pcity_get, ptemp=ptemp_get)
                health.save()
                return redirect('health')

    context = {
        'health_form': health_form
    }
    return render(request, 'deliveryman/createhealth.html', context)


def distribution(request):
    """
    Show the order information distributed to a certain deliveryman
    """
    distribution = Distribution.objects.all()
    distribution_count = distribution.count()
    distribution_p_count = Distribution.objects.filter(status='pending').count()
    distribution_c_count = Distribution.objects.filter(status='confirmed').count()

    if request.is_ajax and request.POST.get('distribution_del'):
        del_distribution_id = request.POST.get('distribution_del')
        del_distribution = Distribution.objects.get(id = del_distribution_id)
        del_distribution.delete()

    context = {
        'distribution_count': distribution_count,
        'distribution_p_count': distribution_p_count,
        'distribution_c_count': distribution_c_count,
        'distribution': distribution
    }
    
    return render(request, 'deliveryman/distribution.html', context)


def confirm_distribution(request, pk):
    """
    Deliveryman confirm the order distributed to himself
    """
    distribution = Distribution.objects.get(id=pk)
    distribution_form = DistributionForm(instance=distribution)

    if request.method == 'POST':
        distribution_form = DistributionForm(request.POST)
        if distribution_form.is_valid():
            dpno_get = distribution_form.cleaned_data['dpno']
            dno_get = distribution_form.cleaned_data['dno']
            username_get = distribution_form.cleaned_data['username']
            status_get = distribution_form.cleaned_data['status']
            distribution = Distribution.objects.filter(id=pk)
            distribution.update(id=pk, dpno=dpno_get, dno=dno_get, username=username_get, status=status_get)
            return redirect('distribution')

    context = {
        'distribution': distribution,
        'distribution_form': distribution_form
    }
    return render(request, 'deliveryman/confirmdistribution.html', context)


def delete_distribution(request, pk):
    """
    Post whether to delete the order distributed to a certain deliveryman
    """
    distribution = distribution.objects.get(id=pk)

    if request.method == 'POST':
        distribution.delete()
        return redirect('distribution')

    context = {
        'distribution': distribution
    }
    return render(request, 'deliveryman/deletedistribution.html', context)
