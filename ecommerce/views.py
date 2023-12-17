from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.contrib import messages
import traceback
import jwt
from .models import USERS
def Dashboard(request):
    try:
        return render(request,"ecomdash.html")
    except:
        traceback.print_exc()