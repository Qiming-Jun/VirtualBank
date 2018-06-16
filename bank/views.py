from django.shortcuts import render
from django.shortcuts import HttpResponse
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
        tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid))
        print("test querynum ",len(tmp))
        for line in tmp:
            print(line.id)
        return render(request,"cardmanage.html",{"inf":tmp})
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













