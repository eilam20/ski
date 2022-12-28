# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from apps.home.forms import OrderCreateModelForm
from apps.home.models import Order


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index', 'all_orders': Order.objects.all(), 'done_orders': Order.objects.filter(done=True),
               'live_orders': Order.objects.filter(done=False).order_by('return_date'), 'past_orders': Order.objects.filter(done=False).filter(return_date__lt=datetime.now())}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {'orders': Order.objects.all()}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


class CreateOrder(CreateView):
    model = Order
    template_name = "home/create.html"
    form_class = OrderCreateModelForm
    success_url = '/'


class EditOrder(UpdateView):
    model = Order
    template_name = "home/update.html"
    form_class = OrderCreateModelForm
    success_url = '/'


def update_order_complete(request, pk):
    # get the model instance
    instance = Order.objects.get(pk=pk)
    # update the field
    instance.done = True
    # save the changes
    instance.save()
    return redirect('/')


def update_order_not_complete(request, pk):
    # get the model instance
    instance = Order.objects.get(pk=pk)
    # update the field
    instance.done = False
    # save the changes
    instance.save()
    return redirect('/')