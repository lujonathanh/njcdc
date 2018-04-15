from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from .forms import InputForm


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
    # request.session["blah"] = "blarg"  # session test code from Changyan
    # request.session.modified = True
    # s = request.session
    # m = s.modified
    # i = s.items()
    # meth = request.method
    if request.method == 'POST':
        input_form = InputForm(request.POST)

        if input_form.is_valid():
            user = input_form.save(commit=False)
            request.session["user"] = user
            messages.success(request, "Thank you for entering")
            request.session.modified = True
            return HttpResponseRedirect(reverse('results'))

        messages.error(request, 'There were errors. Please try again.')
    else:
        input_form = InputForm()

    template = loader.get_template('calc/input.html')
    context = {'input_form': input_form, 'formtitle': "Input"}
    return HttpResponse(template.render(context, request))

def results(request):
    # s = request.session  # session test code from Changyan
    # m = s.modified
    # i = s.items()
    # up = s["user"]
    up = request.session["user"]

    up.calculate_net()

    template = loader.get_template('calc/results.html')
    context = {'up' : up}
    return HttpResponse(template.render(context, request))


    