# -*- encoding: utf-8 -*-
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.home.models import Order


class OrderAsyncAndIndexTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret")
        self.client.login(username="tester", password="secret")
        self.ajax_headers = {"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}

    def test_index_renders_single_order_query_counts(self):
        Order.objects.create(
            name="דני",
            phone="0501234567",
            return_date=date.today() + timedelta(days=2),
            pack=2,
            done=False,
        )
        Order.objects.create(
            name="יוסי",
            phone="0507654321",
            return_date=date.today() - timedelta(days=1),
            pack=1,
            done=True,
        )

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["all_orders"]), 2)
        self.assertEqual(len(response.context["live_orders"]), 1)
        self.assertEqual(len(response.context["done_orders"]), 1)
        self.assertEqual(response.context["total_pack"], 2)

    def test_create_order_ajax_success(self):
        payload = {
            "name": "מיכל",
            "location": Order.LocationChoices.RASHFON,
            "phone": "0521112233",
            "return_date": (date.today() + timedelta(days=3)).isoformat(),
            "pack": 3,
            "notes": "הערה",
        }
        response = self.client.post(
            reverse("order-create"), data=payload, **self.ajax_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["order"]["name"], "מיכל")
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_ajax_validation_error(self):
        payload = {
            "name": "מיכל",
            "location": Order.LocationChoices.RASHFON,
            "phone": "0521112233",
            # missing required return_date
        }
        response = self.client.post(
            reverse("order-create"), data=payload, **self.ajax_headers
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("return_date", data["errors"])
        self.assertEqual(Order.objects.count(), 0)

    def test_edit_order_ajax_success(self):
        order = Order.objects.create(
            name="מיכל",
            phone="0521112233",
            return_date=date.today() + timedelta(days=3),
            pack=2,
        )
        payload = {
            "name": "מיכל מעודכן",
            "location": Order.LocationChoices.NESHER,
            "phone": "0521112233",
            "return_date": (date.today() + timedelta(days=5)).isoformat(),
            "pack": 4,
            "notes": "",
            "done": False,
        }
        response = self.client.post(
            reverse("order-edit", args=[order.pk]), data=payload, **self.ajax_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        order.refresh_from_db()
        self.assertEqual(order.name, "מיכל מעודכן")
        self.assertEqual(order.pack, 4)

    def test_done_and_reopen_order_ajax(self):
        order = Order.objects.create(
            name="רועי",
            phone="0549998877",
            return_date=date.today(),
            pack=1,
            done=False,
        )
        res_done = self.client.post(
            reverse("order-done", args=[order.pk]), **self.ajax_headers
        )
        self.assertEqual(res_done.status_code, 200)
        self.assertTrue(res_done.json()["order"]["done"])

        res_reopen = self.client.post(
            reverse("order-reopen", args=[order.pk]), **self.ajax_headers
        )
        self.assertEqual(res_reopen.status_code, 200)
        self.assertFalse(res_reopen.json()["order"]["done"])
