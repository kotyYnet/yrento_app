from django.shortcuts import render
from project.models import Items , Categories
#from mojerezervacie.models import Reservations
from django.db.models import Count
from .models import About , Rules


def home(request):
    category_list = Categories.objects.all()
    item_list = Items.objects.all()
    template = 'home/home.html'
    context = {
        'category_list_home' : category_list ,
        'item_list_home' : item_list ,
    }

    return render(request , template , context)



def aboutus(request):
    about = About.objects.last()
    template = 'home/about.html'
    context = {
        'about' : about
    }

    return render(request , template , context)


def rulesof(request):
    rules = Rules.objects.last()
    template = 'home/rules.html'
    context = {
        'rules' : rules
    }

    return render(request , template , context)
