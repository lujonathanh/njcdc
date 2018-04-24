from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from .forms import InputForm, UpdatingInputForm
from .models import get_possible_gasoline_units, UserProfile


def index(request):
    template = loader.get_template('calc/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def plot(request):
    template = loader.get_template('calc/plot.html')
    context = {}
    return HttpResponse(template.render(context, request))

def chart(request):
    template = loader.get_template('calc/chart.html')
    context = {}
    return HttpResponse(template.render(context, request))

def about_calc(request):
    template = loader.get_template('calc/about_calc.html')
    context = {}
    return HttpResponse(template.render(context, request))

def about_policy(request):
    template = loader.get_template('calc/about_policy.html')
    context = {}
    return HttpResponse(template.render(context, request))

def input(request):

    if request.method == 'POST':
        print("if")
        input_form = InputForm(request.POST)

        if input_form.is_valid():
            user = input_form.save()

            user.calculate_net()
            # request.session["user"] = user
            # request.session.modified = True
            messages.success(request, "Thank you for entering")

            response = HttpResponseRedirect(reverse('results'))
            response.set_cookie('elec', round(user.elec_cost,2))
            response.set_cookie('gas', round(user.gasoline_cost,2))
            response.set_cookie('heat', round(user.heating_cost,2))
            response.set_cookie('benefit', round(user.benefit,2))

            # delete user profile immediately
            UserProfile.objects.filter(id=user.id).delete()

            return response

        messages.error(request, 'There were errors. Please try again.')
    else:
        input_form = InputForm()

    template = loader.get_template('calc/input.html')
    context = {'input_form': input_form, 'formtitle': "Input"}
    response = HttpResponse(template.render(context, request))
    return response

# def updating_input(request):
#     if request.method == 'POST':
#         input_form = UpdatingInputForm(request.POST)
#
#         if input_form.is_valid():
#             user = input_form.save(commit=False)
#             request.session["user"] = user
#             messages.success(request, "Thank you for entering")
#
#             return HttpResponseRedirect(reverse('results'))
#
#         messages.error(request, 'There were errors. Please try again.')
#     else:
#         input_form = UpdatingInputForm()
#
#     template = loader.get_template('calc/input.html')
#     context = {'input_form': input_form, 'formtitle': "Input"}
#     return HttpResponse(template.render(context, request))

def load_gasoline_units(request):
    possible_units = get_possible_gasoline_units(request.GET.get('gasoline_type'))
    template = loader.get_template('calc/gasoline_unit_dropdown.html')
    context = {'units': possible_units}
    return HttpResponse(template.render(context, request))

# def results(request):
#     up = request.session["user"]

def results(request):
    context = {}

    if 'elec' in request.COOKIES:
        elec = request.COOKIES['elec']
        context['elec'] = elec

    else:
        context['elec'] = {}

    if 'gas' in request.COOKIES:
        gas = request.COOKIES['gas']
        context['gas'] = gas

    else:
        context['gas'] = {}

    if 'heat' in request.COOKIES:
        heat = request.COOKIES['heat']
        context['heat'] = heat

    else:
        context['heat'] = {}

    if 'benefit' in request.COOKIES:
        benefit = request.COOKIES['benefit']
        context['benefit'] = benefit

    else:
        context['benefit'] = {}

    template = loader.get_template('calc/results.html')

    returner = HttpResponse(template.render(context, request))

    return returner

def actions(request):
    context = {}

    if 'elec' in request.COOKIES:
        elec = request.COOKIES['elec']
        context['elec'] = elec

    else:
        context['elec'] = {}

    if 'gas' in request.COOKIES:
        gas = request.COOKIES['gas']
        context['gas'] = gas

    else:
        context['gas'] = {}

    if 'heat' in request.COOKIES:
        heat = request.COOKIES['heat']
        context['heat'] = heat

    else:
        context['heat'] = {}

    if 'benefit' in request.COOKIES:
        benefit = request.COOKIES['benefit']
        context['benefit'] = benefit

    else:
        context['benefit'] = {}

    template = loader.get_template('calc/actions.html')

    returner = HttpResponse(template.render(context, request))

    return returner