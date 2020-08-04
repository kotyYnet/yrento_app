from django.urls import path
from . import views
from djreservation import views as djviews


app_name = 'home'


urlpatterns = [
    path('' , views.home , name='home'),
    path('reservation/list',djviews.ReservationList.as_view(), name='rezervation_list'),
    path('about/',views.aboutus , name='about'),
    path('rules/',views.rulesof , name='pravidla_list'),
]
