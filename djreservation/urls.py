from __future__ import unicode_literals
from django.urls import path , re_path
from . import views
from .settings import TOKENIZE
try:
    from django.conf.urls import url
except:
    from django.urls import re_path as url
from . import views

urlpatterns = [
    path('reservation/create',views.CreateReservation.as_view(), name="add_user_reservation"),
    path('reservation/create/<int:model_pk>',views.CreateReservation.as_view(), name="add_user_reservation_with_pk"),
    path('reservation/finish',views.finish_reservation, name="finish_reservation"),
    url(r'^reservation/delete_product_reservation/(?P<pk>\d+)$', views.deleteProduct, name="delete_product_reservation"),
    path('reservation/list', views.ReservationList.as_view(),name="reservation_list"),
]

if TOKENIZE:
    urlpatterns += [
        url(r'^reservation/token/(?P<pk>\d+)/(?P<token>[0-9a-f-]+)/(?P<status>\d)$',views.update_reservation_by_token,name="reservation_token")
    ]
