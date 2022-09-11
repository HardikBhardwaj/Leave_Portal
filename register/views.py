from django.shortcuts import render,redirect
from .forms import RegisterFrom
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from owner.models import Totalleave,Status
from datetime import date
from datetime import datetime


def register(request):
    objs=Totalleave.objects.values()
    objs1=Status.objects.values()
    if request.method=="POST":
        form=RegisterFrom(request.POST)
        if form.is_valid():
            name=request.POST.get('username')
            id1=request.POST.get('employee_id')
            form.save()
            joining_date=date.today()
            month=joining_date.strftime('%B')
            print(month)
            casual_leave=15
            sick_leave=6
            if month=="Jan":
                casual_leave=15
                sick_leave=6
            if month=="Feb":
                casual_leave=14
                sick_leave=6
            if month=="Mar":
                casual_leave=13
                sick_leave=5
            if month=="Apr":
                casual_leave=11
                sick_leave=5
            if month=="May":
                casual_leave=10
                sick_leave=4
            if month=="Jun":
                casual_leave=9
                sick_leave=4
            if month=="Jul":
                casual_leave=8
                sick_leave=3
            if month=="Aug":
                casual_leave=6
                sick_leave=3
            if month=="Sep":
                casual_leave=5
                sick_leave=2
            if month=="Oct":
                casual_leave=4
                sick_leave=2
            if month=="Nov":
                casual_leave=3
                sick_leave=1
            if month=="Dec":
                casual_leave=1
                sick_leave=1
            print("XXXXXX")
            objs.create(name=name,leaves=casual_leave,sick_leave_alloted=sick_leave)
            objs1.create(employ_id=id1,name=name,sickleave=0,casualleave=0,optionalleave=0,joining_date=joining_date,overday="")
            return redirect('/home')
    else:
        form=RegisterFrom()
    return render(request,"register/register.html",{"form" : form})



