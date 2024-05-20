from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rezerwacje.models import Auto, Rezerwacja, Account
from django.db import transaction
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from rezerwacje.forms import AutoForm, RegistrationForm, AccountAuthenticationForm


# Create your views here.
class AutoListView(ListView):
    model = Auto
    template_name = "index.html"
    queryset = Auto.objects.all()
    context_object_name = "object_list"

    def get_queryset(self):
        return self.queryset.filter(rezerwacja=None)

    def get_context_data(self, **kwargs):
        context = super(AutoListView, self).get_context_data(**kwargs)
        context["form"] = AutoForm(self.request.POST or None)
        return context

    def post(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        form = context["form"]
        if form.is_valid():
            transmission = self.request.POST["transmission"]
            seats = self.request.POST["seats"]
            price = self.request.POST["price"]
            type = self.request.POST["type"]

            if transmission != "":
                self.object_list = self.object_list.filter(transmission=transmission)
            if seats != "":
                self.object_list = self.object_list.filter(seats=seats)
            if price != "":
                self.object_list = self.object_list.filter(price=price)
            if type != "":
                self.object_list = self.object_list.filter(type=type)

            context[self.context_object_name] = self.object_list
        return render(self.request, self.template_name, context)


class AutoDetailView(DetailView):
    model = Auto
    template_name = "detail.html"


class RezerwacjaListView(ListView):
    model = Rezerwacja
    template_name = "rezerwacje.html"


@transaction.atomic
def reserve(request, auto_id):
    auto = Auto.objects.get(id=auto_id)
    if not auto.is_reserved:
        rez = Rezerwacja(auto=auto)
        rez.save()
    return redirect("index")


@transaction.atomic
def unreserve(request, rezerwacja_id):
    try:
        rez = Rezerwacja.objects.get(id=rezerwacja_id)
    except Rezerwacja.DoesNotExist:
        pass
    else:
        rez.delete()
    return redirect("index")


#View for user registration
def registration_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are already authenticated as {user.email}')

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request,account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("/auta")

        else:
            context['registration_form'] = form


    return render(request, 'register.html', context)

#View for user logout
def logout_view(request):
    logout(request)
    return redirect("/auta")

def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("/auta")
    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("/auta")

        else:
            context['login_form'] = form
    return render(request, "login.html", context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect




