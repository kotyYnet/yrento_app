from django.shortcuts import render
from .forms import UserForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'templates/index.html')

@login_required
def special(request):

    return HttpResponse("Ste prihlásený!")

@login_required
def user_logout(request):

    logout(request)

    return render(request,'logout.html')

def register(request):

    registered = False

    if request.method == 'POST':


        user_form = UserForm(data=request.POST)


        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            #user.first_name.save()
            #user.last_name.save()
            user.save()
            registered = True

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
              if user.is_active:

                login(request,user)

                return render(request,'../templates/index.html')
                 #return HttpResponseRedirect(reverse('base.html'))
              else:
                return HttpResponse("Váš účet nie je aktívny.")
        else:
            print("Niekto sa snažil prihlásiť")
            print("Použili meno: {} a heslo: {}".format(username,password))
            return render(request,'../templates/badlog.html')

    else:
        return render(request, 'login.html', {})
