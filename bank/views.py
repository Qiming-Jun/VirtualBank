from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import Template,Context
from bank.models import *
import datetime
#from libsql.models import *
# Create your views here.

def login_html(request):
    return render(request, "login.html")

def login(request):
    if request.method=="POST":
        id = int(request.POST.get("id", None))
        passwd = request.POST.get("passwd", None)
        print(type(id), id, passwd)

        try:
            tmp = Users.objects.get(id=id)
            print(type(passwd), type(tmp.upasswd))
            if tmp.upasswd==passwd:
                print("success!")
                request.session['id'] = id
                request.session['name'] = tmp.uname

                id_get = request.session["id"]
                print("id_get: ",id_get)
                print("test3 exists id : ", request.session.exists("id"))
                return render(request,"user_inf_show.html", {"inf":tmp})
        except:
            print("密码错误或用户名不存在")
        return render(request, "login.html")

       # if passwd_db:
       #     if passwd_db==passwd:
       #         request.session['id'] = id
       #         request.session['name'] =


    #    print("uid ", uid)
     #   return render(request, "login.html")

def logout(request):
    if request.method=="GET":
        request.session.clear()
        return render(request, "login.html")

def viewuserinf(request):
    if request.method=="GET":
        try:
            id_session = request.session["id"]
            tmp = Users.objects.get(id=int(id_session))
            return render(request,"user_inf_show.html",{"inf":tmp})
        except:
            print("登陆状态出错，请重新登陆")
    return render(request,"login.html")

def signup(request):
    if request.method=="GET":
        return render(request, "signup.html")
    if request.method=="POST":
        name = request.POST.get("name", None)
        idcard = request.POST.get("idcard", None)
        phone = request.POST.get("phone", None)
        email = request.POST.get("email", None)
        passwd = request.POST.get("passwd", None)
        paypasswd = request.POST.get("paypasswd", None)
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        user_inf = Users(uname=name,uidcard=idcard,uphone=phone,uemail=email,
                         upasswd=passwd,paypasswd=paypasswd,time=time)
        user_inf.save()

        print("id, name ", id, name)
        return render(request, "login.html")

def edituserinf(request):
    if request.method=="GET":
        #print("test2 exists id : ", request.session.exists("id"))
        id_session = request.session.get("id", None)
        if id_session:
            try:
                tmp = Users.objects.get(id=int(id_session))
                return render(request,"user_inf_edit.html",{"inf":tmp})
            except:
                print("登陆状态出错，请重新登陆")
        return render(request,"login.html")
    if request.method=="POST":
        try:
            id_session = request.session["id"]

            name = request.POST.get("name", None)
            idcard = request.POST.get("idcard", None)
            phone = request.POST.get("phone", None)
            email = request.POST.get("email", None)
            Users.objects.filter(id=int(id_session)).update(uname=name,uphone=phone,uemail=email)

            tmp = Users.objects.get(id=int(id_session))
            return render(request, "user_inf_show.html", {"inf": tmp})

        except:
            print("error 1: 登陆状态出错，请重新登陆")
    return render(request,"login.html")

def cardmanage(request):
    if request.method=="GET":
     #   try:
        uid = request.session["id"]
        tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid)).values_list("id","time","balance","status")
      #  list=[tmp[0],tmp[1]]
      #  tmp = Context({"inf":CrashCard.objects.all()})
      #  print(tmp[0].id,tmp, type(tmp))
        print(locals())
        return render(request,"cardmanage.html",locals())
      #  except:
       #     return render(request,"login.html")
    return render(request,"login.html")

def showcardinsert(request):
    if request.method=="GET":
        return render(request, "addcard.html")

def addcard(request):
    if request.method=="POST":
     #   try:
        id_session = int(request.session["id"])
        paypasswd_sql = Users.objects.get(id=id_session).paypasswd
        paypasswd_html = request.POST.get("paypasswd")

        if paypasswd_html==paypasswd_sql:
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tmp = CrashCard(user=Users.objects.get(id=id_session),time=time)
            tmp.save()

            inf = "添加成功，卡号为" + str(tmp.id)
            return render(request,"addcard_success.html",{"inf":(inf,)})
        else:
            inf = "支付密码验证失败"
            return render(request,"addcard_success.html",{"inf":(inf,)})
      #  except:
       #     return render(request,"login.html")
    else:
        return render(request,"inf.html",{"inf":("非法登入！",)})

def transfer(request):
    if request.method== "GET":
        try:
            uid = request.session["id"]
            tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid)).\
                values_list("id", "time", "balance","status")
            print(locals())
            return render(request, "transfer.html", locals())
        except:
            return render(request, "login.html")
    if request.method== "POST":
        try:
            uid = request.session["id"]
        except:
            return render(request, "login.html")

        uid = request.session["id"]
        paypasswd_html = request.POST.get("paypasswd", None)
        paypasswd_sql = Users.objects.get(id=uid).paypasswd
        print("paypasswd：",paypasswd_html, paypasswd_sql)
        if paypasswd_sql!=paypasswd_html:
            return render(request, "inf.html", {"inf":("支付密码错误",)})
            #return HttpResponse("支付密码错误！")
   #     try:
        scard = int(request.POST.get("scard", None))
        dcard = int(request.POST.get("dcard", None))
        amount = float(request.POST.get("amount", None))
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        scbalance = CrashCard.objects.get(id=scard).balance
        dcbalance = CrashCard.objects.get(id=dcard).balance

        if scbalance<amount:
            return render(request, "inf.html", {"inf": "余额不足", })
        print("error 01")

        tmp1 = Transfer(time=time,
                       scard=CrashCard.objects.get(id=scard),
                       dcard=CrashCard.objects.get(id=dcard),
                       suser=Users.objects.get(id=uid),
                       duser=Users.objects.get(id=CrashCard.objects.get(id=dcard).user.id),
                       amount=amount,
                       scbalance=CrashCard.objects.get(id=scard).balance-amount,
                       dcbalance=CrashCard.objects.get(id=dcard).balance+amount
                       )
        print("error 02")
        CrashCard.objects.filter(id=scard).update(balance=scbalance-amount)
        #tmp2[0].balance -= amount
        CrashCard.objects.filter(id=dcard).update(balance=dcbalance+amount)
        #tmp3[0].balance += amount
        print("error 03")

        tmp1.save()
     #   tmp2[0].save()
      #  tmp3[0].save()
        print("error 04")
    #    except:
     #       return HttpResponse("转账出错，请检查卡号")
        tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid)).values_list("id", "time", "balance", "status")
        return render(request, "cardmanage.html", locals())



"""
def transfer(requset):
    if requset.method=="GET":
        try:
            uid = requset.session["id"]
            tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid)).\
                values_list("id", "time", "balance","status")
            print(locals())
            return render(requset,"transfer.html",locals())
        except:
            return render(requset,"login.html")
    if requset.method=="POST":
        try:
            uid = requset.session["id"]
        except:
            return render(requset,"login.html")

        uid = requset.session["id"]
        paypasswd_html = requset.POST.get("paypasswd",None)
        paypasswd_sql = Users.objects.get(id=uid).paypasswd
        print("paypasswd：",paypasswd_html, paypasswd_sql)
        if paypasswd_sql!=paypasswd_html:
            #return render(requset,"inf.html",{"inf":("支付密码错误",)})
            return HttpResponse("支付密码错误！")
   #     try:
        scard = int(requset.POST.get("scard",None))
        dcard = int(requset.POST.get("dcard", None))
        amount = float(requset.POST.get("amount",None))
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        scbalance = CrashCard.objects.get(id=scard).balance
        dcbalance = CrashCard.objects.get(id=dcard).balance

        if scbalance<amount:
            return HttpResponse("余额不足！")
        print("error 01")

        tmp1 = Transfer(
                       scard=CrashCard.objects.get(id=scard),
                       dcard=CrashCard.objects.get(id=dcard),
                       suser=Users.objects.get(id=uid),
                       duser=Users.objects.get(id=CrashCard.objects.get(id=dcard).user),
                       amount=amount,
                       scbalance=CrashCard.objects.get(id=scard).balance-amount,
                       dcbalance=CrashCard.objects.get(id=dcard).balance+amount
                       )
        print("error 02")
        tmp2 = CrashCard.objects.filter(id=scard)
        tmp2[0].balance -= amount
        tmp3 = CrashCard.objects.filter(id=dcard)
        tmp3[0].balance += amount
        print("error 03")

        tmp1.save()
        tmp2.save()
        tmp3.save()
        print("error 04")
    #    except:
     #       return HttpResponse("转账出错，请检查卡号")

        return HttpResponse("支付密码错误 2")
"""













