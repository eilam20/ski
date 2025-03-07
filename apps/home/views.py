# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64
from datetime import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from apps.home.forms import OrderCreateModelForm, OrderUpdateModelForm
from apps.home.models import Order
from django.contrib.auth import authenticate
from django.db.models import Sum

@login_required(login_url="/login/")
def index(request):
    live_orders = Order.objects.filter(done=False).order_by('return_date')
    total_pack = live_orders.aggregate(Sum('pack'))['pack__sum'] or 0
    context = {
        'segment': 'index',
        'all_orders': Order.objects.all(),
        'done_orders': Order.objects.filter(done=True),
        'live_orders': live_orders,
        'past_orders': Order.objects.filter(done=False, return_date__lt=datetime.now()),
        'total_pack': total_pack
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def all_orders(request):
    context = {'segment': 'all_orders', 'all_orders': Order.objects.filter(done=False)}
    html_template = loader.get_template('home/all_orders.html')
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
    form_class = OrderUpdateModelForm
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



def get_pending_orders(request):
    auth_header = request.headers.get("Authorization", "")

    if auth_header.startswith("Basic "):
        # Extract and decode credentials
        auth_encoded = auth_header.split(" ")[1]
        auth_decoded = base64.b64decode(auth_encoded).decode("utf-8")
        username, password = auth_decoded.split(":")

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            pending_orders = Order.objects.filter(done=False).order_by('return_date').values("id", "name", "phone", "location", "return_date", "pack")
            return JsonResponse(list(pending_orders), safe=False)

    return JsonResponse({"error": "Unauthorized"}, status=401)