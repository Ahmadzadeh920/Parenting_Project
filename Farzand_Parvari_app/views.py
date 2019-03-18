# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User,Permission,Group
from datetime import datetime
import requests
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from rest_framework import generics
from rest_framework.exceptions import APIException,PermissionDenied,ValidationError
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import Children, request_consultant
from .Serializer import (User_serialize,
                        Profile_Parents_serialize,
                        Profile_psy_serilalize,
                        )
# Create your views here.

def validate_request(request, keys):
    for key in keys:
        if key not in request.data:
            raise APIException('request.data missing key "{}"'.format(key))
        if request.data[key] == '':
            raise APIException('request.data missing value "{}"'.format(key))
    return True


def validate_password(password,user=None):
    min_length=8
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not any(char.isdigit() for char in password):
        raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': min_length})
    if not any(char.isalpha() for char in password):
        raise ValidationError(_('Password must contain at least %(min_length)d letter.') % {'min_length': min_length})
    if not any(char in special_characters for char in password):
        raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {'min_length': min_length})
    return True



# check the user is member of groups
# user is objective
# group is name of groups(string)
def is_member(user , group_name):
    if user.groups.filter(name__in=[group_name]).exists():
        return True
    else:
        return False


@csrf_exempt
def check_member(request):
    member=is_member(request.user,'Parents')
    if member:
        return JsonResponse({'message':member})
    else:
        return JsonResponse({'message': 'Not member'})
# located the user this groups
# user is objective
# group is name of groups(string)
def located_user_groups(user,groups):
    if not Group.objects.filter(name=groups).exists():
        my_group=Group.objects.create(name=groups)
    else:
        my_group = Group.objects.get(name=groups)
    located=my_group.user_set.add(user)
    return located

# Validations of File size
def validate_file_size(value):
    filesize = value.size
    if filesize > 2097152:
        raise ValidationError("The maximum file size that can be uploaded is 2MB")
    elif filesize < 10240:
        raise ValidationError("The Minimum file size that can be uploaded is 10K")
    else:
        return True

def _add_user(request,is_parents,is_psychology,is_admin):
   if request.method=='POST':
       if validate_request(request,('username','password', 'email', 'first_name' , 'last_name' , 'password_confirm')):
           username=request.data['username']
           password=request.data['password']
           email=request.data['email']
           first_name=request.data['first_name']
           last_name=request.data['last_name']
           password_confirm=request.data['password_confirm']
           validators_password=validate_password(password)
           if password == password_confirm and len(password)>8 and validators_password:
               if not User.objects.filter(email=email).exists():  # check the email is exists
                   if not User.objects.filter(username=username).exists():  # check the email is exists
                       make_pass= make_password(password)
                       date=datetime.now()
                       if is_admin==True:
                           data_user={
                               'first_name':first_name,
                               'last_name':last_name,
                               'last_login':date,
                               'is_superuser':True,
                               'username':username,
                               'password':make_pass,
                               'email':email,
                               'is_staff':True,
                               'is_active':True,
                               'date_joined':date,
                           }
                           serilizer_admin=User_serialize(data=data_user)
                           if serilizer_admin.is_valid():
                                serilizer_admin.save()
                                User_obj=User.objects.get(username=username)
                                located=located_user_groups(User_obj,'Admin')
                                status=201
                                massage='Successfully registerations Admin'
                           else:
                               status=422
                               massage='UnSuccessfully, Serialize is not valid'
                       if is_parents == True or is_psychology==True:
                            data_user = {
                                'first_name': first_name,
                                'last_name': last_name,
                                'last_login': date,
                                'is_superuser': False,
                                'username': username,
                                'password': make_pass,
                                'email': email,
                                'is_staff': False,
                                'is_active': True,
                                'date_joined': date,
                            }
                            serilizer_user=User_serialize(data=data_user)
                            if serilizer_user.is_valid():
                               serilizer_user.save()
                               User_obj = User.objects.get(username=username)
                               if is_parents==True:
                                    located = located_user_groups(User_obj, 'Parents')
                                    status=201
                                    massage='Successsfully , register parents is completed '
                               if is_psychology==True:
                                   located = located_user_groups(User_obj, 'Psychology')
                                   status=201
                                   massage='Successsfully , register psychology is completed '
                   else:
                       status = 400
                       massage = 'username is exist please enter diffrent username'
               else:
                   status=400
                   massage='email is exist please enter diffrent emails'
           else:
               status=400
               massage='Password and confirm password is not equal and length of password must be more than 8'
       else:
           massage='inputs must not to be empty'
           status=400
   else:
       massage='method request is not valid'
       status=405
   return JsonResponse({'message': massage},status=status)


# Create Admin Sait
@csrf_exempt
@api_view(['POST'])
def Create_admin_site(request):
    #if request.user.is_authenticated() and request.user.is_superuser :
    return _add_user(request, False, False , True)
    #else:
        #raise PermissionDenied()

@csrf_exempt
@api_view(['POST','GET'])
def register_parents(request):
   return _add_user(request, True, False , False)

@csrf_exempt
@api_view(['POST',])
def register_psychology(request):
   return _add_user(request, False, True , False)

def belong_FileNumber_User(user,file_number):
    file_number=int(file_number)
    queryset=Children.objects.filter(Parent=user, file_number=file_number)
    if queryset.exists():
        return True
    else:
        return False
############ Permission via groups belong to user
# user is object of user
def Check_Permission_groups(user, txt_permission): # tx_permission is format 'app_label.permission codename' in auth_permissions table
    if txt_permission=='Farzand_Parvari_app.List':
        return True
    elif user.has_perm(txt_permission):# example of txt txt_permission 'app_name.can_add_cost_price'
        return True
    else:
        return False


def belong_FileNumber_User(user,file_number): # parents
        file_number=int(file_number)
        queryset=Children.objects.filter(Parent=user, file_number=file_number)
        if queryset.exists():
            return True
        else:
            return False



def belong_FileNumber_Psy(user,file_number):
    if is_member(user,'Psychology'):
        file_number=int(file_number)
        queryset_1=request_consultant.objects.filter(user_psy=user, file_number=file_number  ,activ_req=2)
        queryset_2=request_consultant.objects.filter(user_psy=user, file_number=file_number  ,activ_req=1)
        if queryset_1.exists() or queryset_2.exists():
            return True
        else:
            return False
    else:
        raise PermissionDenied

def belong_FileNumber_Psy_activate(user,file_number):
    if is_member(user,'Psychology'):
        file_number=int(file_number)
        queryset=request_consultant.objects.filter(user_psy=user, file_number=file_number  ,activ_req=2)
        if queryset.exists():
            return True
        else:
            return False
    else:
        raise PermissionDenied








def Check_Permissions_Request_User(user,file_number,txt_permission):
    txt_permission='Farzand_Parvari_app.'+txt_permission
    if belong_FileNumber_User(user,file_number):
        return True
    elif belong_FileNumber_Psy(user,file_number):
        if Check_Permission_groups(user,txt_permission) or txt_permission=='Farzand_Parvari_app.List' :
            return True
        else:
            return False
    else:
        return False



#______________________________Chat


import websocket
#ws = websocket.WebSocket()
#ws.connect("ws://http://localhost:8080/login/")











