from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.template import Template,Context
from bank.models import *
import pymysql as MySQLdb
import datetime
import rsa
import os
import bank.tools as tools

def login_html(request):
    file_path = os.path.abspath(__file__)
    file_path = "\\".join(file_path.split("\\")[:-1])
    print(file_path)
    with open(file_path+"\\public.pem", 'r') as f:
        tmp = f.read()
        pubkey = rsa.PublicKey.load_pkcs1(tmp)
    with open(file_path+"\\private.pem", 'r') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read())

    cry = rsa.encrypt("aaa".encode(),pubkey)
    print("rsssssssssa: ", cry)
    print("mmmmmmmmmmm: ", rsa.decrypt(cry,privkey))
    return render(request, "login.html")

"""
def login(request):
    if request.method=="GET":
        return render(request,"login.html")

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
        return render(request, "login.html")    """

def login(request):
    if request.method=="GET":
        return render(request, "login.html")

    if request.method=="POST":
        id = int(tools.DecodeDecrypt(request.POST.get("id", None)).decode())
        passwd = tools.DecodeDecrypt(request.POST.get("passwd", None)).decode()
        print(type(id), id, type(passwd), passwd)

        try:
            tmp = Users.objects.get(id=id)
            print(type(passwd), type(tmp.upasswd))
            if tmp.upasswd==passwd:
                print("success!")
                request.session['id'] = id
                request.session['name'] = tmp.uname

                return HttpResponse("success")
        except:
            return HttpResponse("密码错误或用户名不存在!")
            print("密码错误或用户名不存在!")
        return render(request, "login.html",)

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
    return render(request, "login.html")

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

        print("id, name ", user_inf.id, name)
       # return render(request, "login.html")
        inf = "注册成功，id为 "+str(user_inf.id)
        return HttpResponse(inf)

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
        return render(request, "login.html")
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
    return render(request, "login.html")

def cardmanage(request):
    if request.method=="GET":
     #   try:
        uid = request.session["id"]
        tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid))
        print(tmp)
        return render(request,"cardmanage.html",{"card_list":tmp})
      #  except:
       #     return render(request, "login.html")
    return render(request, "login.html")


def cardmanage1(request):
    if request.method=="GET":
     #   try:
        uid = request.session["id"]
        tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid)).values_list("id","time","balance","status")
      #  list=[tmp[0],tmp[1]]
      #  tmp = Context({"inf":CrashCard.objects.all()})
      #  print(tmp[0].id,tmp, type(tmp))
        print(locals())
        return render(request,"cardmanage1.html",locals())
      #  except:
       #     return render(request, "login.html")
    return render(request, "login.html")

def showcardinsert(request):
    if request.method=="GET":
        return render(request, "addcard.html")

def addcard(request):
    if request.method=="POST":
        try:
            id_session = int(request.session["id"])
            paypasswd_sql = Users.objects.get(id=id_session).paypasswd
            print(request.POST.get("paypasswd"))
            paypasswd_html = tools.DecodeDecrypt(request.POST.get("paypasswd")).decode()

            if paypasswd_html==paypasswd_sql:
                time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                tmp = CrashCard(user=Users.objects.get(id=id_session),time=time)
                tmp.save()

                inf = "添加成功，卡号为" + str(tmp.id)
                return HttpResponse([1,inf])
            else:
                inf = "支付密码验证失败"
                return HttpResponse([0,inf])
        except:
            return HttpResponse([2,"0"])
    else:
        return render(request,"inf.html",{"inf":("非法登入！",)})


def transfer1(request):
    if request.method== "GET":
        try:
            uid = request.session["id"]
            #tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid)).\
            #    values_list("id", "time", "balance","status")

            tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid))

            print(locals())
            return render(request, "transfer.html", {'card_list2':tmp})
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
        tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid))
        return render(request, "cardmanage.html", {'card_list':tmp})

def transfer(request):
    if request.method== "GET":
        try:
            uid = request.session["id"]
            tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid))
            print(locals())
            return render(request, "transfer.html", {"card_list2":tmp})
        except:
            return render(request, "login.html")
    if request.method== "POST":
        try:
            uid = request.session["id"]
        except:
            return render(request, "login.html")

        uid = request.session["id"]
        paypasswd_html = tools.DecodeDecrypt(request.POST.get("paypasswd", None)).decode()
        paypasswd_sql = Users.objects.get(id=uid).paypasswd
        print("paypasswd：", paypasswd_html, paypasswd_sql)
        if paypasswd_sql!=paypasswd_html:
            #return render(requset,"inf.html",{"inf":("支付密码错误",)})
            return HttpResponse("支付密码错误！")
        try:
            scard = int(tools.DecodeDecrypt(request.POST.get("scard", None)))
            dcard = int(tools.DecodeDecrypt(request.POST.get("dcard", None)))
            amount = float(tools.DecodeDecrypt(request.POST.get("amount", None)))
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            scbalance = CrashCard.objects.get(id=scard).balance
            dcbalance = CrashCard.objects.get(id=dcard).balance

            if scbalance<amount:
                return HttpResponse("余额不足！")
            print("error 01")

            tmp1 = Transfer(time=time,
                            scard=CrashCard.objects.get(id=scard),
                            dcard=CrashCard.objects.get(id=dcard),
                            suser=Users.objects.get(id=uid),
                            duser=Users.objects.get(id=CrashCard.objects.get(id=dcard).user.id),
                            amount=amount,
                            scbalance=CrashCard.objects.get(id=scard).balance - amount,
                            dcbalance=CrashCard.objects.get(id=dcard).balance + amount
                            )
            print("error 02")
            CrashCard.objects.filter(id=scard).update(balance=scbalance - amount)
            # tmp2[0].balance -= amount
            CrashCard.objects.filter(id=dcard).update(balance=dcbalance + amount)
            # tmp3[0].balance += amount
            print("error 03")

            tmp1.save()
            #   tmp2[0].save()
            #  tmp3[0].save()
            print("error 04")
        except:
            return HttpResponse("转账出错，请检查卡号")

        return HttpResponse("success")

def viewtransfer(request):
    if request.method=="GET":
        try:
            uid = request.session["id"]
        except:
            return render(request, "login.html")
        uid = request.session["id"]
        db = tools.sqlconnect()
       # db = db_tmp[0]
        cursor = db.cursor()
        sql = """select bank_transfer.id,uname,scard_id,dcard_id,amount,bank_transfer.time,
              bank_users.id,bank_transfer.suser_id
        from bank_users,bank_crashcard,bank_transfer
        where bank_users.id=bank_crashcard.user_id
          and bank_users.id=%d
          and (bank_transfer.scard_id=bank_crashcard.id 
            or bank_transfer.dcard_id=bank_crashcard.id)
        group by bank_transfer.id"""%(uid)
        cursor.execute(sql)
        tmp = cursor.fetchall()

        return render(request,"viewtransfer.html",{"transfer_list":tmp})

def userdeposit(request):
    if request.method=="GET":
        try:
            uid = request.session["id"]
        except:
            return render(request, "login.html")
        return render(request,"userdeposit.html")

    elif request.method=="POST":
        try:
            uid = request.session["id"]
        except:
            return render(request, "login.html")
        uid = request.session["id"]
      #  try:
        card = int(request.POST.get("card",None))
        amount = float(request.POST.get("amount", None))
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_balance = CrashCard.objects.get(id=card).balance+amount
        tmp = DrawDeposit(card=CrashCard.objects.get(id=card),
                    amount=amount,
                    type="存款",
                    balance=new_balance,
                    time=time
                    )
        tmp.save()
        CrashCard.objects.filter(id=card).update(balance=new_balance)
        return HttpResponse("操作成功")
 #   except:
      #      return HttpResponse("存款错误，请检查卡号或金额")
    return render(request, "login.html")

def userdraw(request):
    if request.method=="GET":
        try:
            uid = request.session["id"]
            tmp = CrashCard.objects.filter(user=Users.objects.get(id=uid))
            return render(request, "userdraw.html", {"card_list3":tmp})
        except:
            return render(request, "login.html")

    elif request.method=="POST":
        try:
            uid = request.session["id"]
        except:
            return render(request, "login.html")
        uid = request.session["id"]

        print(request.POST.get("paypasswd", None))
        paypasswd_html = tools.DecodeDecrypt(request.POST.get("paypasswd", None)).decode()
        paypasswd_sql = Users.objects.get(id=uid).paypasswd
        print("paypasswd：", paypasswd_html, paypasswd_sql)
        if paypasswd_sql != paypasswd_html:
            return HttpResponse("支付密码错误")

        card = int(tools.DecodeDecrypt(request.POST.get("card", None)))
        amount = float(tools.DecodeDecrypt(request.POST.get("amount", None)))

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_balance = CrashCard.objects.get(id=card).balance - amount

        if uid != CrashCard.objects.get(id=card).user_id:
            return HttpResponse("您没有这张银行卡")
        if new_balance < 0:
            return HttpResponse("余额不足，无法取款")

        tmp = DrawDeposit(card=CrashCard.objects.get(id=card),
                          amount=amount,
                          type="取款",
                          balance=new_balance,
                          time=time
                          )
        tmp.save()
        CrashCard.objects.filter(id=card).update(balance=new_balance)
        return HttpResponse("success")
    return render(request, "login.html")

def viewdrawdeposit(request):
    if request.method=="GET":
        try:
            uid = request.session["id"]
        except:
            return render(request, "login.html")
        uid = request.session["id"]
        db = tools.sqlconnect()
        cursor = db.cursor()
        sql = """select bank_drawdeposit.id,card_id,amount,bank_drawdeposit.balance,
              type,datafrom,bank_drawdeposit.time
        from bank_users,bank_crashcard,bank_drawdeposit
        where bank_users.id=bank_crashcard.user_id
          and bank_users.id=%d
          and bank_drawdeposit.card_id=bank_crashcard.id"""%(uid)
        cursor.execute(sql)
        tmp = cursor.fetchall()

        return render(request,"viewdrawdeposit.html",{"drawdeposit_list":tmp})
    else:
        return render(request, "login.html")














