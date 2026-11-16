# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64
from datetime import date

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from apps.home.forms import OrderCreateModelForm, OrderUpdateModelForm
from apps.home.models import Order
from django.contrib.auth import authenticate


def _is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _serialize_order(order):
    return {
        "id": order.pk,
        "order_date": order.order_date.strftime("%d-%m-%Y") if order.order_date else "",
        "name": order.name or "",
        "phone": order.phone or "",
        "location": order.get_location_display(),
        "return_date": order.return_date.strftime("%d-%m-%Y") if order.return_date else "",
        "pack": order.pack,
        "done": order.done,
    }


@login_required(login_url="/login/")
def index(request):
    context = {
        'segment': 'index',
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dashboard_orders_api(request):
    today = date.today()
    all_orders = list(
        Order.objects.only(
            'id', 'order_date', 'return_date', 'name', 'phone', 'location', 'pack', 'done'
        ).order_by('return_date')
    )
    live_orders = [o for o in all_orders if not o.done]
    past_count = sum(1 for o in live_orders if o.return_date and o.return_date < today)
    total_pack = sum(o.pack for o in live_orders if o.pack)

    return JsonResponse({
        "counts": {
            "all": len(all_orders),
            "live": len(live_orders),
            "past": past_count,
            "total_pack": total_pack,
        },
        "orders": [_serialize_order(o) for o in all_orders],
    })

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


class AjaxFormResponseMixin:
    success_message = "נשמר בהצלחה!"

    def form_valid(self, form):
        self.object = form.save()
        if _is_ajax(self.request):
            return JsonResponse({
                "success": True,
                "message": self.success_message,
                "order": _serialize_order(self.object),
                "redirect_url": str(self.get_success_url()),
            })
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        if _is_ajax(self.request):
            return JsonResponse({
                "success": False,
                "message": "לא ניתן לשמור — יש לתקן את השדות המסומנים.",
                "errors": form.errors,
            }, status=400)
        return super().form_invalid(form)


class CreateOrder(AjaxFormResponseMixin, CreateView):
    model = Order
    template_name = "home/create.html"
    form_class = OrderCreateModelForm
    success_url = '/'
    success_message = "ההזמנה נוצרה בהצלחה!"


class EditOrder(AjaxFormResponseMixin, UpdateView):
    model = Order
    template_name = "home/update.html"
    form_class = OrderUpdateModelForm
    success_url = '/'
    success_message = "ההזמנה עודכנה בהצלחה!"


def update_order_complete(request, pk):
    instance = get_object_or_404(Order, pk=pk)
    instance.done = True
    instance.save(update_fields=['done'])
    if _is_ajax(request):
        return JsonResponse({
            "success": True,
            "message": f"ההזמנה של {instance.name or ''} סומנה כהוחזרה.",
            "order": _serialize_order(instance),
        })
    return redirect('/')


def update_order_not_complete(request, pk):
    instance = get_object_or_404(Order, pk=pk)
    instance.done = False
    instance.save(update_fields=['done'])
    if _is_ajax(request):
        return JsonResponse({
            "success": True,
            "message": f"ההזמנה של {instance.name or ''} נפתחה מחדש.",
            "order": _serialize_order(instance),
        })
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