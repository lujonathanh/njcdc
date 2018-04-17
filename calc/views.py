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

def about(request):
    template = loader.get_template('calc/about.html')
    context = {}
    return HttpResponse(template.render(context, request))

def input(request):

    if request.method == 'POST':
        input_form = InputForm(request.POST)

        if input_form.is_valid():
            user = input_form.save()


            # FOR SESSIONS, UNCOMMENT THE BELOW
            # user = input_form.save(commit=False)
            # request.session["user"] = user
            # request.session.modified = True
            messages.success(request, "Thank you for entering")


            return HttpResponseRedirect(reverse('results', kwargs={'id': user.id}))

        messages.error(request, 'There were errors. Please try again.')
    else:
        input_form = InputForm()

    template = loader.get_template('calc/input.html')
    context = {'input_form': input_form, 'formtitle': "Input"}
    return HttpResponse(template.render(context, request))


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

def results(request, id):
    up = UserProfile.objects.get(id=id)

    up.calculate_net()

    template = loader.get_template('calc/results.html')
    context = {'up' : up}

    returner = HttpResponse(template.render(context, request))

    UserProfile.objects.filter(id=id).delete()

    return returner


    