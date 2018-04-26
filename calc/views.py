from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from .forms import InputForm, UpdatingInputForm
from .models import *


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

    gasoline_example_type = ('e10', 'Regular Gasoline')
    gasoline_example_label = gasoline_example_type[1]
    gasoline_example_unit = 'gallon'
    gasoline_example_co2 = get_gasoline_co2_conversion(gasoline_example_type,
                                                       gasoline_example_unit)
    gasoline_example_amt = 1
    gasoline_example_fee = round(FEE * get_gasoline_co2(gasoline_example_type, gasoline_example_amt,
                                        gasoline_example_unit), 2)


    household_example_adults = 2
    household_example_children = 2

    household_example_benefit, benefit_per_adult = get_benefit_for_household(emissions=ANNUALEMISSIONS/12.0,
                                                                             fee=FEE,
                                                                             rebate_portion=REBATE_PORTION,
                                                                             adult_population=ADULT_POPULATION,
                                                                             child_population=UNDER18_POPULATION,
                                                                             child_multiplier=CHILD_MULTIPLIER,
                                                                             household_adults=household_example_adults,
                                                                             household_children=household_example_children)


    admin_cost_label = "3%"

    context = {'fee_label': "$" + str(FEE), 'rebate_label': str(int(REBATE_PORTION * 100)) + "%",
               'remainder_label': str(int(100 - REBATE_PORTION * 100)) + "%",
               'CHILD_MULTIPLIER': CHILD_MULTIPLIER,
               'gasoline_example_label': gasoline_example_label,
               'gasoline_example_co2': '%.1E' % gasoline_example_co2,
               'gasoline_example_unit': gasoline_example_unit,
               'gasoline_example_fee': gasoline_example_fee,
               'household_example_adults': household_example_adults,
               'household_example_children': household_example_children,
               'household_example_benefit': "$" + str(int(round(household_example_benefit))),
               'benefit_per_adult': "$" + str(int(round(benefit_per_adult)))
               }
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

            if user.total_cost == 0:
                response = HttpResponseRedirect(reverse('results0'))
                response.set_cookie('total_cost', user.total_cost)
                response.set_cookie('net', int(user.net))
            else:
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
    context = {'input_form': input_form, 'formtitle': "Input",
               'gasoline_unit': DEFAULT_GASOLINE_UNIT_CHOICE[1],
               'elec_unit': DEFAULT_ELEC_UNIT_CHOICE[1]}
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
    keys = ['elec', 'gas', 'heat', 'benefit']

    for key in keys:
        if key in request.COOKIES:
            context[key] = request.COOKIES[key]
        else:
            context[key] = {}

    template = loader.get_template('calc/results.html')

    return HttpResponse(template.render(context, request))


def results0(request):
    context = {}
    keys = ['elec', 'gas', 'heat', 'benefit', 'total_cost', 'net']

    for key in keys:
        if key in request.COOKIES:
            context[key] = request.COOKIES[key]
        else:
            context[key] = {}

    template = loader.get_template('calc/results0.html')

    return HttpResponse(template.render(context, request))


def actions(request):
    context = {}
    keys = ['elec', 'gas', 'heat', 'benefit']

    for key in keys:
        if key in request.COOKIES:
            context[key] = request.COOKIES[key]
        else:
            context[key] = {}

    template = loader.get_template('calc/actions.html')

    return HttpResponse(template.render(context, request))
