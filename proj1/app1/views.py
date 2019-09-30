from django.shortcuts import render
from django.http import HttpResponse
from app1.models import student
from app1.forms import studentform
# Create your views here.

def hello(request):
    return HttpResponse("hello")


def dataview(request):
    rec=student.objects.all()
    return render(request,'data.html',{'rec':rec})


def formview(request):
    if request.method=='POST':
        form=studentform(request.POST)
        if form.is_valid():
            form.save()
    form=studentform()
    return render(request,'form.html',{'form':form})