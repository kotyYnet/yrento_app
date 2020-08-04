from django.shortcuts import render, get_object_or_404,\
    redirect
from django.views.generic.edit import CreateView
from .models import Product, Reservation, ReservationToken
from .forms import ProductForm, ReservationForm
from django.http.response import HttpResponseRedirect, Http404
try:
    from django.core.urlresolvers import reverse
except:
    from django.urls import reverse

from django.utils.translation import ugettext_lazy as _
from .email import send_reservation_email
from django.views.generic.list import ListView

from django.contrib import messages

# Create your views here.

from .settings import (END_RESERVATION_DATETIME,
                       START_RESERVATION_DATETIME,
                       TOKENIZE)

from project.models import Items

def get_base_url(request):
    protocol = request.is_secure() and 'https://' or 'http://'
    domain = request.META['HTTP_HOST']
    return protocol + domain


class ReservationList(ListView):
    model = Reservation
    paginate_by = 10

    def get_queryset(self):
        queryset = ListView.get_queryset(self)
        queryset = queryset.filter(user=self.request.user).exclude(
            status=Reservation.BUILDING).order_by('-updated_datetime', 'status')
        return queryset


class CreateReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = "/reservation/finish"

    def get_context_data(self, **kwargs):
        context = super(CreateReservation, self).get_context_data(**kwargs)
        context['iem_list'] = Items.objects.all()
        return context

    def get_initial(self):
        pkmodel = self.kwargs['model_pk']
        item = Items.objects.get(pk=pkmodel)
        initial = {
        'itemi': item,

        }
        return initial

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return super(CreateReservation, self).get_success_url()

    def get_success_view(self):
        response = HttpResponseRedirect(self.get_success_url())
        response.set_cookie("reservation", str(self.object.pk))
        return response

    def get_form_class(self):
        form = CreateView.get_form_class(self)

        form.request = self.request
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        if TOKENIZE:
            ReservationToken.objects.create(
                reservation=self.object,
                base_url=get_base_url(self.request))
        send_reservation_email(self.object, self.request.user)

        messages.success(self.request, _('Reservation created'))

        return self.get_success_view()





def finish_reservation(request):
    if not hasattr(request, 'reservation'):
        raise Http404(_("No reservation object started"))

    if request.method == "GET":
        response = render(
            request,
            'djreservation/reservation_confirm.html',
            {"reservation": request.reservation})
    elif request.method == "POST":
        reservation = request.reservation
        reservation.status = reservation.REQUESTED
        reservation.save()
        request.reservation = None
        send_reservation_email(reservation, request.user)
        response = render(
            request, 'djreservation/reservation_finished.html')
        response.set_cookie("reservation", "0")
        messages.success(request, _('Reservation finised'))
    return response





class ProductReservationView(CreateView):
    model = Product
    base_model = None
    amount_field = None
    extra_display_field = None
    form_class = ProductForm
    success_url = "/"

    def get_success_view(self):
        return HttpResponseRedirect(self.get_success_url())

    def get_available_amount(self):
        return getattr(self.instance, self.amount_field)

    def get_extra_fields(self):
        extra_fields = []
        for field in self.extra_display_field:
            if hasattr(self.instance, "get_%s_display" % field):
                value = getattr(self.instance, "get_%s_display" % field)()
            else:
                value = getattr(self.instance, field)
            extra_fields.append({
                'label': self.instance._meta.get_field(
                    field).verbose_name,
                'value': value
            })
        return extra_fields

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)

        context['extra_fields'] = self.get_extra_fields()
        context["instance"] = self.instance
        context["available_amount"] = self.get_available_amount()
        return context

    def form_valid(self, form):
        self.object = Product(
            amount=form.cleaned_data['amount'],
            amount_field=self.amount_field,
            reservation=self.request.reservation,
            content_object=self.instance,

        )
        self.object.save()
        messages.success(self.request, _('Product added successful'))
        return self.get_success_view()

    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        kwargs['initial']['model_instance'] = str(self.instance.pk)
        kwargs['initial']["available_amount"] = self.get_available_amount()
        return kwargs

    def get(self, request, *args, **kwargs):
        if "modelpk" in kwargs:
            model_pk = kwargs.pop("modelpk")
            self.instance = self.base_model.objects.get(pk=model_pk)
        return CreateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "modelpk" in kwargs:
            model_pk = kwargs.pop("modelpk")
            self.instance = self.base_model.objects.get(pk=model_pk)
        elif "model_instance" in request.POST:
            self.instance = self.base_model.objects.get(
                pk=request.POST.get("model_instance"))

        return CreateView.post(self, request, *args, **kwargs)


def deleteProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, _('Product deleted successful'))
    return redirect(reverse("finish_reservation"))


def update_reservation_by_token(request, pk, token, status):
    token_reservation = get_object_or_404(ReservationToken, reservation=pk,
                                          token=token)
    status_available = list(dict(Reservation.STATUS).keys())
    if int(status) not in status_available:
        raise Http404()

    reservation = token_reservation.reservation

    if int(status) == Reservation.ACCEPTED :
        reservation.product_set.all().update(borrowed=True)
    reservation.status = status
    reservation.save()
    token_reservation.delete()
    messages.success(request, _('Reservation updated successful'))
    return redirect("/")
