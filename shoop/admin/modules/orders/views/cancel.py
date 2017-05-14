from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView

from shoop.core.models import Order
from shoop.core.models._orders import OrderStatusRole


class OrderCancelView(DetailView):
    model = Order

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.status.role == OrderStatusRole.CANCELED:
            self.object.set_canceled()
        return redirect(reverse("shoop_admin:order.detail", kwargs={"pk": self.object.id}))
