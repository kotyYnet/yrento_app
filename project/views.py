from django.shortcuts import render
from .models import Items , Categories , Dormitories
from django.db.models import Q
from django.contrib.auth.models import User
from djreservation.views import ProductReservationView
from djreservation.models import Reservation
from django.utils import timezone
import datetime

class MyObjectReservation(ProductReservationView):
    base_model = Items    # required
    amount_field = 'quantity'  # required



def hme(request):
    lit_object = Items.objects.all()
    template = 'item/indx.html'
    context = {
            'lst_object': lit_object
        }
    return render(request , template , context)


# Create your views here.
def dorm_list(request):
    dorm_list = Dormitories.objects.all()
    template = 'item/list.html'

    dorm_query = request.GET.get('d')
    print(dorm_list)
    context = {
        'dorm_list' : dorm_list
    }


    return render(request , template , context)



def item_list(request):
    item_list = Items.objects.all()
    item_end = Reservation.objects.all()
    DateTimeField = datetime.datetime.now()
    template = 'item/list.html'
    testo = Items.status

    print(testo)

    search_name = request.GET.get('q', None)
    dormitory_id = request.GET.get('dom_list', None)
    if dormitory_id :
        print(dormitory_id)
        item_list = item_list.filter(Q(dormitory_id=dormitory_id[0])).distinct()
    elif search_name:
        print(search_name)
        item_list= item_list.filter(Q(name=search_name)).distinct()



    print(item_list)
    context = {
        'item_list' : item_list,
        'item_end': item_end ,
                }

    return render(request , template , context)


def item_detail(request, id):
    item_detail = Items.objects.get(id=id)
    DateTimeField = datetime.datetime.now()
    template = 'item/detail.html'

    item_all = Reservation.objects.all()
    item_end = item_all.filter(itemi=id, reserved_end_date__gt=DateTimeField).first()
    item_reser = item_all.filter(itemi=id, reserved_end_date__gt=DateTimeField)
    item_zoznam = item_all.filter(itemi=id, reserved_end_date__lt=DateTimeField)

    if request.method == 'POST':
        reserve_form = ReserveForm(request.POST)
        if reserve_form.is_valid():
            reserve_form.save()


    context = {
        'item_detail' : item_detail ,
        'item_all': item_all ,
        'item_end': item_end ,
        'item_reser': item_reser ,
        'item_zoznam': item_zoznam  ,


    }

    return render(request , template , context)
