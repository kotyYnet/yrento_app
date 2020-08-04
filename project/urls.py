from django.urls import path,  re_path
from . import views
from djreservation import urls as djreservation_urls
from .views import hme, MyObjectReservation


app_name = 'item'


urlpatterns = [
    path('inventar/',views.item_list , name='item_list'),
    path('inventar/<int:id>',views.item_detail , name='item_detail'),
    path('',views.dorm_list , name='dorm_list'),
    re_path('reservation/create/<int:modelpk>',
            MyObjectReservation.as_view(), name="myreservation")
] + djreservation_urls.urlpatterns
