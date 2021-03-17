from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead
# Create your views here.

def lead_list(request):
    #return HttpResponse("Hello World")
    leads=Lead.objects.all()
    context={
        "leads":leads
    }
    return render(request,'lead_list.html',context)
def lead_detail(request,pk):
    print(pk)

    return HttpResponse(f"This is the detailed View {pk}")