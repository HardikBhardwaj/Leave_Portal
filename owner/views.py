from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import AdminUser,Status,optional,compulsary,Totalleave,forgot
from django.utils.dateparse import parse_date
from django.db.models import F
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date
from datetime import datetime,timedelta
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def home(request):
     return redirect('/login')
     return render(request,{})
def home1(request):
     print("zmhc jk")
     # return redirect('/login')
     try:
          currentusername=request.user.username
          objs=" "
          remainingSickLeave=6
          remainingCasualLeave=0
          if Status.objects.filter(name=currentusername).exists():
               objs=Status.objects.values().get(name=currentusername)
           
         
          objs3=15
          carryleave=0
          if Totalleave.objects.filter(name=currentusername).exists():
               objs3=Totalleave.objects.values().get(name=currentusername)
               if  objs3['sick_leave_alloted'] is not None:
                    remainingSickLeave=int(objs3['sick_leave_alloted'])-int(objs['sickleave'])
               carryleave=objs3['leaves']
               if(carryleave<16):
                    carryleave=0
                    remainingCasualLeave=int(objs3['leaves'])-int(objs['casualleave'])
               else:
                    carryleave=carryleave-15
                    remainingCasualLeave=int(objs3['leaves'])-int(objs['casualleave'])
          if int(objs['casualleave'])<0:
               casual_leave=int(objs['casualleave'])
               remainingCasualLeave=remainingCasualLeave
               objs3['leaves']=remainingCasualLeave
               objs['casualleave']=0
     except:
          objs=""
          objs3=""
          carryleave=""
          remainingCasualLeave=""
          remainingSickLeave=""
          
     return render(request,"owner/base.html",{"objs":objs,"objs3" : objs3,"carryleave" : carryleave,'remainingCasualLeave' :remainingCasualLeave,'remainingSickLeave':remainingSickLeave})

def adminview(request):
#     userinfo=AdminUser.objects.all()
    return render(request,"owner/front.html",{})
    # return HttpResponse("suhaib shamshad")

def leavepolicy(request):
#     userinfo=AdminUser.objects.all()
    return render(request,"owner/leavepolicy.html",{})

def showdata(request):
     objs1=Status.objects.values()
     objs2=Totalleave.objects.values()
     for item in objs1:
          if item['joining_date']!=None:
               item['joining_date']=item['joining_date'].strftime('%Y/%m/%d')
     return render(request,"owner/showdata.html",{"objs1" : objs1,"objs2":objs2})


def forreason1(request):
     objs=AdminUser.objects.values()
     objs1=Status.objects.values()
     objs2=User.objects.values()
     objs4=optional.objects.values()
     objs5=compulsary.objects.values()
     if request.method=='POST':
          name=request.POST.get('accept')
          check="xxxxxxxxxxxxxxx"
          Addindecline="xxxxxxx"
          print(name)
          print("PPP")
          x1=request.POST.get('decline')
          print(x1)
          if x1 is not None:
               n10=Addindecline+x1
               Addindecline=n10.split(":")
               print(type(Addindecline))
               check=Addindecline[0]
               print(len(Addindecline))
               if len(Addindecline)==1:
                    print("!")
                    Addindecline.append(",")
                    print("@")
               print("XX")
               print(Addindecline)
               message=Addindecline[1]
               
          print(check)     
          if check[7:14]=="decline":
               print("zzzzzz")
               a=AdminUser.objects.get(name=check[14:])
               a.delete()
             
               x2=objs2.get(username=check[14:])
               useremail=x2['email']
               emaildecline(useremail,message)
          else:
               print("ZZZZ")
               Adminobj=(objs.get(name=name))
               todate=Adminobj['to']
               n5=Adminobj['from1']
               from1=n5
               n6=todate-n5
               n6=n6.days
               n6=int(n6)
               n6=n6+1
               z=0
               y2=objs2.get(username=name)
               
               y3=y2['email']
               print(y3)
               str=from1.strftime('%d/%m/%Y') + " to  " + todate.strftime('%d/%m/%Y')
               print(y3,str)
               emailaccept(y3,str)
               for x in range(n6):
                    x1=n5.weekday()
                    if x1 is 5:
                         z=z+1
                    if x1 is 6:
                         z=z+1
                    if x1 is not 5 and x1 is not 6:
                         if compulsary.objects.filter(compulsaryleave=n5).exists():
                             z=z+1
                         if Status.objects.filter(name=name).exists():
                              x2=(objs1.get(name=name))
                              x3=x2['optionalleave']
                              if x3<1:
                                   if optional.objects.filter(optionalleave=n5).exists():
                                        objs1.filter(name=name).update(optionalleave=1)
                                        z=z+1
                    n5=n5+ datetime.timedelta(days=1)
               n6=n6-z
               n7=Adminobj['status1']
               if Status.objects.filter(name=name).exists():
                    
                    if n7=="casualleave":
                         objs1.filter(name=name).update(casualleave=F('casualleave') + n6)
                    if n7=="sickleave":
                         objs1.filter(name=name).update(sickleave=F('sickleave') + n6)
                    if n7=="optionalleave":
                         if n6 is 1:
                              objs1.filter(name=name).update(optionalleave=1)
               x2=objs2.get(username=name)
               x3=x2['email']
               print(x3)
               
               a=AdminUser.objects.get(name=name)
               a.delete()
     return render(request,"owner/forreason.html",{'objs': objs , "objs1" : objs1})

def holiday(request):
     objs=optional.objects.values()
     objs1=compulsary.objects.values()
     if request.method == "POST":
          n=request.POST.get('optional')
          n1=request.POST.get('compulsary')
          n5=request.POST.get('delete')
          n7=request.POST.get('delete1')
          if n5 is None:
               n5="kk"
          if n7 is None:
               n7="kk"
          if n=='optional':
               n3=request.POST.get('optionalleave')
               discrO=request.POST.get('descriptionO')
               temp_date1 = parse_date(n3)
               objs.create(optionalleave=temp_date1,description=discrO)
          if n1=='compulsary':
               n4=request.POST.get('compulsaryleave')
               discrC=request.POST.get('descriptionC')
               temp_date2 = parse_date(n4)
               objs1.create(compulsaryleave=temp_date2,description=discrC)
          if n5[0:2]=='cc':
               a=compulsary.objects.get(id=n5[2:])
               a.delete()
          if n7[0:2]=='oo':
               a=optional.objects.get(id=n7[2:])
               a.delete()
     return render(request,"owner/holiday.html",{"objs" : objs,"objs1" :objs1})





def leave(request):
     objs5=User.objects.values()
     objs=AdminUser.objects.values()
     objs6=User.objects.values()
     username=request.user.username
     noofopl=0
     employeeemail='suhaib@knowlvers.com'
     if Status.objects.filter(name=username).exists():
          objs1=Status.objects.values().get(name=username)
          a3=objs6.get(username=username)
          employeeemail=a3['email']
          noofopl=objs1['optionalleave']
     if request.method=="POST":
          n=username
          email1=request.POST.getlist('name')
          i=0
          list=[]
          list.append('jessica@knowlvers.com')
          lengthemail = len(email1)
          for i in range(lengthemail):
               emailname=email1[i]
               r2=objs6.get(username=emailname)
               emailadd=r2['email']
               list.append(emailadd)
               i=i+1
          n1=request.POST.get('reason')
          n2=request.POST.get('from1')
         
          temp_date1 = parse_date(n2)
          n3=request.POST.get('to')
          temp_date2 = parse_date(n3)
          n4=request.POST.get('name1')
          print(n4)
          if n1 in [None, '']:  
               return HttpResponse("<h1>Please mention the reason.</h1>")
          if temp_date1 is None:
               return HttpResponse("<h1>Please mention   'From'  date</h1>")
          if  temp_date2 is None:
               return HttpResponse("<h1>Please mention   'To'   date</h1>")
          date = datetime.date.today()
          print(date)      
          n5=temp_date1
          todate=temp_date2
          n6=todate-n5
          n6=n6.days
          n6=int(n6)
          
          i=0
          print(list)
          lengthemail = len(list)
       
          if(n4=="optionalleave"):
               if n6==0:
                    if optional.objects.filter(optionalleave=n5).exists():
                         print()
                    else:
                         return HttpResponse("<h1>You mentioned wrong date</h1>")

          n6=n6+1
          if n6 < 0:
               return HttpResponse("<h1>You mentioned wrong date</h1>")
              
          z=0
          comp=0
          opt=0
          
          
          for x in range(n6):
               x1=n5.weekday()
               if x1 is 5:
                    z=z+1
               if x1 is 6:
                    z=z+1
               if x1 is not 5 and x1 is not 6:
                    if compulsary.objects.filter(compulsaryleave=n5).exists():
                        z=z+1
                        comp=comp+1
                    if Status.objects.filter(name=n).exists():
                        
                         if noofopl<1:
                              if optional.objects.filter(optionalleave=n5).exists():
                                   z=z+1
                                   noofopl=1
                                   opt=1
               n5=n5+ datetime.timedelta(days=1)
          n6=n6-z
          n6= "totalleave = " +str(n6) + "|| " + " compulsory holidays " +  str(comp) +"|| " + " optional holidays " +  str(opt)  
          if(n4=="sickleave"):
               if AdminUser.objects.filter(name=n).exists():
                    objs.filter(name=n).update(reason=n1)
                    objs.filter(name=n).update(from1=temp_date1)
                    objs.filter(name=n).update(to=temp_date2)
                    objs.filter(name=n).update(status1=n4)
                    objs.filter(name=n).update(noofdays=n6)
               else:
                    objs.create(name=n,reason=n1,from1=temp_date1,to=temp_date2,status1=n4,noofdays=n6)
          if(n4=="casualleave"):
               if AdminUser.objects.filter(name=n).exists():
                    print("XX")
                    todaydate =  datetime.date.today()
                    leavenegative=temp_date1-todaydate
                    if leavenegative.days < 0:
                         return HttpResponse("<h1>You mentioned wrong date</h1>")
                    objs.filter(name=n).update(reason=n1)
                    objs.filter(name=n).update(from1=temp_date1)
                    objs.filter(name=n).update(to=temp_date2)
                    objs.filter(name=n).update(status1=n4)
                    objs.filter(name=n).update(noofdays=n6)
               else:
                    todaydate =  datetime.date.today()
                    leavenegative=temp_date1-todaydate
                    if leavenegative.days < 0:
                         return HttpResponse("<h1>You mentioned wrong date</h1>")
                    objs.create(name=n,reason=n1,from1=temp_date1,to=temp_date2,status1=n4,noofdays=n6)
          if(n4=="optionalleave"):
               if AdminUser.objects.filter(name=n).exists():
                    objs.filter(name=n).update(reason=n1)
                    objs.filter(name=n).update(from1=temp_date1)
                    objs.filter(name=n).update(to=temp_date2)
                    objs.filter(name=n ).update(status1=n4)
                    objs.filter(name=n).update(noofdays=n6)
               else:
                    objs.create(name=n,reason=n1,from1=temp_date1,to=temp_date2,status1=n4,noofdays=n6)
          print("xyz")
          for i in range(lengthemail):
               emailname=list[i]
               email(employeeemail,n,emailname,temp_date1,temp_date2,n1)
               i=i+1     
          return HttpResponse("<h1> We have received your leave request. Once the decision gets made, the status will be sent to your registered email address.</h1>")
          return redirect("/home")
     return render(request,"owner/reason.html",{"noofopl" : noofopl,"objs5" : objs5})



def overwork(request):
     objs=User.objects.values()
     objs1=Status.objects.values()
     if request.method=="POST":
          n=request.POST.get('name')
          n1=request.POST.get('date')
          temp_date1 = parse_date(n1)
          # value=date.today()-temp_date1
          value=date.today()-temp_date1
          value=int(value.days)
          if(value<1):
               return HttpResponse("<h1>You mentioned wrong date</h1>")
             
          n1=n1+"  "
          if Status.objects.filter(name=n).exists():
               objs1.filter(name=n).update(casualleave=F('casualleave') -1)
               x=objs1.get(name=n)
               x1=x['overday']
               if(len(x1)>2):
                    x1=x1+' , ' + n1
               else:
                    x1=n1;
               objs1.filter(name=n).update(overday=x1)
          else:
               objs1.create(name=n,sickleave=0,casualleave=-1,optionalleave=0,overday=n1)
          return redirect('/showdata')


     return render(request,"owner/overwork.html",{"objs":objs})

def delete(request):
     objs=User.objects.values()
     objs1=Totalleave.objects.values()
     if request.method=="POST":
          n=(request.POST.get('delete'))
          a=User.objects.get(username=n)
          b=Totalleave.objects.get(name=n)
          c=Status.objects.get(name=n)
          a.delete()
          b.delete()
          c.delete()
          
          
     return render(request,"owner/delete.html",{"objs":objs})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'owner/changepassword.html', {
        'form': form
    })
def reset(request):
     objs=Totalleave.objects.values()
     objs1=Status.objects.values()
     for item1 in objs:
          name=item1['name']
          if Status.objects.filter(name=name).exists():
               item=objs1.get(name=name)
               leavetaken=item['casualleave']
               leaveremain=objs.filter(name=name)
               leaveincr=15-leavetaken
               if leaveincr > 0:
                    leaveitem=objs.get(name=name)
                    totalleaveincr=leaveincr+leaveitem['leaves']
                    if totalleaveincr < 40 :
                         objs.filter(name=name).update(leaves=totalleaveincr)
                    else:
                         objs.filter(name=name).update(leaves=39)
               else:
                    objs.filter(name=name).update(leaves=15)
               objs1.filter(name=name).update(sickleave=0)
               objs1.filter(name=name).update(casualleave=0)
               objs1.filter(name=name).update(optionalleave=0)
               objs1.filter(name=name).update(overday=" ")
          else:
               leave=item1['leaves']
               leave=15+leave
               if(leave<40):
                    objs.filter(name=name).update(leaves=leave)
               else:
                    objs.filter(name=name).update(leaves=39)
     return render(request,"owner/front.html",{})



import random
def forgot1(request):
     objs=User.objects.values()
     objs1 = forgot.objects.all()
     if request.method == 'POST':
          name=(request.POST.get('name'))
          if User.objects.filter(username=name).exists():
               print("suhaib")
               otp= random.randint(0,1000000000000)
               if forgot.objects.filter(name=name).exists():
                    objs1.filter(name=name).update(otp=otp)
               else:
                    objs1.create(name=name,otp=otp)
               x2=objs.get(username=name)
               x3=x2['email']
               emailpassword(x3,otp)
               return redirect('/forgotsave')
          else:
               return HttpResponse("<h1>not valid username</h1>")
     return render(request,"owner/forgot.html",{})
def forgotsave(request):
     objs= User.objects.values()
     objs1 = forgot.objects.values()
     if request.method == 'POST':
          name=(request.POST.get('name'))
          otp=(request.POST.get('otp'))
          pass1=(request.POST.get('pass1'))
          pass2=(request.POST.get('pass2'))
          if forgot.objects.filter(name=name,otp=otp).exists():
               if pass1==pass2:
                    user, created = User.objects.get_or_create(username=name)
                    user.set_password(pass1)
                    user.save()
                    c=forgot.objects.get(name=name)
                    c.delete()
                    return HttpResponse("<h1>password is successefully change</h1>")
               else:
                    return HttpResponse("<h1>password fields are not same</h1>")
          else:
               return HttpResponse("<h1>worng name or OTP</h1>")
     return render(request,"owner/forgotsave.html",{})

def showholiday(request):
     objs=optional.objects.values()
     objs1=compulsary.objects.values()
     return render(request,"owner/showholiday.html",{"objs" : objs,"objs1":objs1})

def email(n1,n,x,from_date,to_date,reason):
     import smtplib
     from email.mime.multipart import MIMEMultipart
     from email.mime.text import MIMEText
     # AWS Config
     EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
     EMAIL_HOST_USER = "AKIAWQQ7CW4Q3E46EGHK" # Replace with your SMTP username
     EMAIL_HOST_PASSWORD = "BLAzzBd188PHsK1y1tja++sd0bNOuMQL68sIPuyLgJht" # Replace with your SMTP password
     EMAIL_PORT = 587
     print(n1)
     
     print(x)
     print(reason)
     msg = MIMEMultipart('alternative')
     msg['Subject'] =  'Applied for leave from ' + str(from_date) + ' to ' + str(to_date)
     msg['From'] = n1
     msg['To'] = x
     print(n1,'body',from_date,to_date)
     body = 'Hello,\n\n This is to inform that ' + n +' has applied for leave from ' + str(from_date) + ' to ' + str(to_date) + '\n Reason'+' -  '+ reason +'. \n\n Regards,\n Knowlvers Consulting'
     body = MIMEText(body) # convert the body to a MIME compatible string
     msg.attach(body) # attach it to your main message
     s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
     s.starttls()
     print("MM")
     s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
     print(msg['From'])
     print(msg['To'])
     print("XX")
     s.sendmail(msg['From'],msg['To'], msg.as_string())
     print("YY")
     s.quit()
     print("zz")


def emaildecline(x,y):
     import smtplib
     from email.mime.multipart import MIMEMultipart
     from email.mime.text import MIMEText
     #AWS Config
     EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
     EMAIL_HOST_USER = "AKIAWQQ7CW4Q3E46EGHK" # Replace with your SMTP username
     EMAIL_HOST_PASSWORD = "BLAzzBd188PHsK1y1tja++sd0bNOuMQL68sIPuyLgJht" # Replace with your SMTP password
     EMAIL_PORT = 587

     msg = MIMEMultipart('alternative')
     print(x)
     msg['Subject'] = 'Leave application not approved.'
     msg['From'] = "jessica@knowlvers.com"
     msg['To'] = x
     body = 'Hello, \n\n Please note that your leave has not been Approved. \nReason - ' + y + '\n\n\n Regards, \n Knowlvers Consulting,'
     body = MIMEText(body) # convert the body to a MIME compatible string
     msg.attach(body) # attach it to your main message
     s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
     s.starttls()
     s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
     s.sendmail(msg['From'], msg['To'], msg.as_string())
     s.quit()




def emailaccept(x3,str):
     import smtplib
     from email.mime.multipart import MIMEMultipart
     from email.mime.text import MIMEText
     #AWS Config
     EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
     EMAIL_HOST_USER = "AKIAWQQ7CW4Q3E46EGHK" # Replace with your SMTP username
     EMAIL_HOST_PASSWORD = "BLAzzBd188PHsK1y1tja++sd0bNOuMQL68sIPuyLgJht" # Replace with your SMTP password
     EMAIL_PORT = 587

     msg = MIMEMultipart('alternative')
      
     print(x3,str)
     msg['Subject'] = 'Leave application  approved. '
     msg['From'] = "jessica@knowlvers.com"
     msg['To'] = x3
     body = 'Hello, \n\n Please note that your leave  application from  '  + str + ' has been accepted. \n\n Regards \n Knowlvers Consulting'
     body = MIMEText(body) # convert the body to a MIME compatible string
     msg.attach(body) # attach it to your main message
     s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
     s.starttls()
     s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
     s.sendmail(msg['From'], msg['To'], msg.as_string())
     s.quit()

def emailpassword(x,y):
     print("XXXXX")
     import smtplib
     from email.mime.multipart import MIMEMultipart
     from email.mime.text import MIMEText
     #AWS Config
     EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
     EMAIL_HOST_USER = "AKIAWQQ7CW4Q3E46EGHK" # Replace with your SMTP username
     EMAIL_HOST_PASSWORD = "BLAzzBd188PHsK1y1tja++sd0bNOuMQL68sIPuyLgJht" # Replace with your SMTP password
     EMAIL_PORT = 587
     msg = MIMEMultipart('alternative')
     msg['Subject'] = 'Forgot Password'
     msg['From'] = "jessica@knowlvers.com"
     msg['To'] = x
     body = 'Hello,\n\n ' + str(y) + '  is your OTP to change the password of your account. \n\n Regards,\n Knowlvers Consulting,'
     body = MIMEText(body) # convert the body to a MIME compatible string
     msg.attach(body) # attach it to your main message
     print("ss")
     print(x)
     s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
     s.starttls()
     s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
     print("PP")
     s.sendmail(msg['From'], msg['To'], msg.as_string())
     s.quit()
     print("hh")