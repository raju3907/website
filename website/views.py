from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.contrib import messages
import traceback
import jwt
from . import models
from.models import USERS
from.Login import access_token
from django.conf import settings

def Login(request):
    try:
        return render(request,"welcome.html")

    except:
        traceback.print_exc()
def signup(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            mobile = request.POST["mobile"]
            if USERS.objects.filter(username=username).count() > 0:
                return HttpResponse("Username already exist")
            if len(mobile) != 10:
                return HttpResponse("Please Enter 10 digit mobile number")
            new_user = USERS.objects.create(username=username,password=password)
            new_user.mobile=mobile
            new_user.firstname = firstname
            new_user.lastname = lastname

            new_user.save()
            print("user created")



            return redirect("signin")

        print ("Signup done")
        return render(request,"signup.html")
    except Exception as e:
        print(e)
        traceback.print_exc()
def signin(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            try:
                print("checking credentials")
                user=USERS.objects.get(username=username,password=password)
                print(user.firstname)
                accesstoken=access_token(user.username)
                resp=redirect('Home')
                resp.set_cookie('Authorization',accesstoken,max_age=259200)
                return resp
            except:
                traceback.print_exc()
                messages.error(request, "Invalid Credentails")

        print("signin")
        return render(request, "signin.html")

    except Exception as e:
        print(e)
        traceback.print_exc()
def Home(request):
    try:
        print("Home page")
        id=request.COOKIES.get('Authorization')
        decode_json = jwt.decode(id, settings.SECRET_KEY, algorithms='HS256')
        id_ = decode_json["username"]
        user=USERS.objects.get(username=id_)
        data={
            "firstname":user.firstname,
            "lastname":user.lastname,
            "username":user.username
        }
        print(user.firstname,"firstname")
        return render(request,"Home.html",data)
    except Exception as e:
        print(e)
        traceback.print_exc()

def signout(request):
    try:
        resp = redirect('signin')
        resp.set_cookie('Authorization', "")
        return resp

    except:
        traceback.print_exc()