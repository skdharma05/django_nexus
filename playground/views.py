from django.shortcuts import render
from django.http import HttpResponse

def calculator():
    x =1
    y =2
    return x
# Create your views here.
def say_hello(request):
    x=calculator()
    return render(request,'hello.html',{'name':'Dharma'})