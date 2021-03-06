from django.shortcuts import render,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Lead,Agent
from .forms import LeadForm,LeadModelForm,CustomUserCreationView
from django.views import generic
#TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
# Create your views here.


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'

    form_class = CustomUserCreationView

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

def landing_page(request):
    return render(request, 'landing.html')

class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name = 'lead_list.html'
    queryset = Lead.objects.all()   #Context default value is object_list
    context_object_name = 'leads'

def lead_list(request):
    #return HttpResponse("Hello World")
    leads=Lead.objects.all()
    context={
        "leads":leads
    }
    return render(request,'lead_list.html',context)

class LeadDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = 'lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'

def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context={
        "lead":lead
    }

    return render(request,'lead_detail.html',context)

class LeadCreateView(LoginRequiredMixin,generic.CreateView):
    template_name = 'lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    def form_valid(self, form):
        #TODO Send Email
        send_mail(
            subject="A Lead has been created",
            message="Go to the site of the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]

        )
        return super(LeadCreateView,self).form_valid(form)



def lead_create(request):
    form=LeadModelForm()     # Initiated a LeadForm object

    if request.method=="POST":
        form=LeadModelForm(request.POST)         #POST allows for model data to be submitted

    if form.is_valid():         #checked for form validity
        form.save()             # Created a new instance and saved the model data
        return redirect('/leads')
    context={
        "form":form
    }
    return render(request, 'lead_create.html',context)

class LeadUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'lead_update.html'
    form_class = LeadModelForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)  #LeadForm object with the preloaded lead object

    if request.method == "POST":
        form = LeadModelForm(request.POST,instance=lead)  # POST allows for model data to be submitted


    if form.is_valid():  # checked for form validity
        form.save()  # Created a new instance and saved the model data
        return redirect('/leads')
    context = {
        'form': form,
        'lead': lead
    }
    return render(request, 'lead_update.html', context)

class LeadDeleteView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'lead_delete.html'
    queryset = Lead.objects.all()
    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(request,pk):
    lead=Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')




"""def lead_update(request,pk):
    lead= Lead.objects.get(id=pk)
    form = LeadForm()  # Initiated a LeadForm object

    if request.method == "POST":
        form = LeadForm(request.POST)  # POST allows for model data to be submitted

    if form.is_valid():  # checked for form validity

        first_name = form.cleaned_data["first_name"]  # .cleaned_data to retrieve in a more readable way
        last_name = form.cleaned_data["last_name"]
        age = form.cleaned_data["age"]

        lead.first_name=first_name
        lead.last_name=last_name
        lead.age=age

        lead.save()
        return redirect('/leads')
    context={
        'form':form,
        'lead':lead
        }
    return render(request,'lead_update.html',context)
"""

"""def lead_create(request):
    form=LeadForm()     # Initiated a LeadForm object

    if request.method=="POST":
        form=LeadForm(request.POST)         #POST allows for model data to be submitted

    if form.is_valid():         #checked for form validity


        first_name=form.cleaned_data["first_name"]        #.cleaned_data to retrieve in a more readable way
        last_name=form.cleaned_data["last_name"]
        age=form.cleaned_data["age"]
        agent=Agent.objects.first()         # Use the first agent as our parameter

        Lead.objects.create(     #Created a lead with the help of a form
            first_name=first_name,
            last_name=last_name,
            age=age,
            agent=agent
        )

        return redirect('/leads')
    context={
        "form":form
    }
    return render(request, 'lead_create.html',context)"""
