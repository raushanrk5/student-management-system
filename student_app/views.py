from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .EmailBackend import EmailBackend
from django.contrib.auth import login,logout
from django.contrib import messages
from  django.urls import reverse

# Create your views here.
def demo(request):
    return render(request,"index.html")

def show_login(request):
    return render(request, 'login.html')

def dologin(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        user = EmailBackend.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : " + request.user.email+ "usertype: " + request.user.user_type)
    else:
        return HttpResponse('Login First!!')

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')