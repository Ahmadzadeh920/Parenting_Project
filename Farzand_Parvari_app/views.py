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
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes
from rest_framework import generics
from rest_framework.exceptions import APIException,PermissionDenied,ValidationError
from rest_framework.permissions import IsAdminUser,IsAuthenticated
#import Chat_app.views as views_chat_online
from django.contrib.auth.models import Group


from django.db.models import Q
from .models import (
                        Profile_Parents,
                        ProfilePsy,
                        Children,
                        Steps_training,
                        Steps_exercise,
                        Comments_FileNumber_Training,
                        Answer_Exercise,
                        Children_behavior,
                        Descript_behavior,
                        record_behavior_Weekly,
                        Cause_list,
                        Cause_file_number,
                        Rewards,
                        type_of_Rewrard,
                        Rewards_behavior,
                        Rules_Reward,
                        Star_Table,
                        Surprice_Table,
                        punishment_recommend,
                        Punishment_behavior,
                        Situation_defficult_behavior,
                        request_consultant,
                        Agenda_fileNumber,
                        Set_Time_Cost_filenumber,
                        Answer_question_request,
                        notting_fileNumber,
                        general_noting,
                        Helper_file_number
                            )

from .Serializer import (User_serialize,
                        Profile_Parents_serialize,
                        Profile_psy_serilalize,
                        )

from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def Index(request):

    return render(request, 'index.html')


def handler404(request, *args, **argv):
    response = render_to_response('404.html', {},)
    response.status_code = 404
    return response


def handler400(request, *args, **argv):
    response = render_to_response('400.html', {},)
    response.status_code = 400
    return response

def handler500(request, *args, **argv):
    response = render_to_response('500.html', {},)
    response.status_code = 403
    return response





def validate_request(request, keys):
    for key in keys:
        if key not in request.data:
            #raise APIException('request.data missing key "{}"'.format(key))
             return True
        if request.data[key] == '':
            #raise APIException('request.data missing value "{}"'.format(key))
            return True
    return True


def validate_password(password,user=None):
    min_length=8
    special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
    if not any(char.isdigit() for char in password):
        #raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': min_length})
        message = 'پسورد  باید شامل حداقل یک عدد باشد'
        return False,message
    if not any(char.isalpha() for char in password):
        #raise ValidationError(_('Password must contain at least %(min_length)d letter.') % {'min_length': min_length})
        message = 'پسوردباید شامل حداقل یک حرف باشد'
        return False, message
    if not any(char in special_characters for char in password):
        #raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {'min_length': min_length})
        message = 'پسورد حداقل باید شامل یک کارکتر خاص باشد'
        return False, message
    return True , None




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

def _add_user(request,is_parents,is_psychology,is_admin,is_helper):
   role='والد'
   if is_helper:
       role='همیار'
   elif is_admin:
       role='ادمین'
   elif is_psychology:
       role = "مشاور"
   if request.method=='POST':
       if validate_request(request,('username','password', 'email', 'first_name' , 'last_name' , 'password_confirm')):
           username=request.data['username']
           password=request.data['password']
           email=request.data['email']
           first_name=request.data['first_name']
           last_name=request.data['last_name']
           password_confirm=request.data['password_confirm']
           validators_password=validate_password(password)
           check_validators_password=validators_password[0]
           validate_password_message=validators_password[1]
           if check_validators_password:
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
                           if is_parents == True or is_psychology==True or is_helper==True:
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
                                        massage=' لطفا پس از ورود به حساب کاربری پروفایل خود را تکمیل فرمایید '

                                   if is_psychology==True:
                                       located = located_user_groups(User_obj, 'Psychology')
                                       status=201
                                       massage=' برای فعال سازی کاربری شما باید پروفایل خود را تکمیل فرمایید '

                                   if is_helper==True:
                                       located = located_user_groups(User_obj, 'Helper')
                                       status = 201
                                       massage = ' ثبت نام شما به عنوان همیار با موفقیت انجام شد '

                       else:
                           status = 400
                           massage = 'نام کاربری موجود است لطفا نام کاربری خود را تغییر دهید'
                   else:
                       status=400
                       massage='ایمیل موجود است لطفا ایمیل خود را  تغییر دهید '
               else:
                   status=400
                   massage='حئاقل طول پسور باید 8 کاراکتر باشد و پسوردها با هم یکسان نمی باشند'
           else:
               massage = validate_password_message
               status=400
       else:
           massage='ورودی ها نباید خالی باشد'
           status=400
   else:
       massage='به صفحه ثبت نام خوش آمدید'
       status=405

   if status == 201 :
        tempalte_name= 'login.html'
   else:
        tempalte_name = 'register.html'

   return render(request,tempalte_name,{'message': massage , 'role': role , 'status':status })


# Create Admin Sait

@api_view(['POST' , 'GET'])
def Create_admin_site(request):
    #if request.user.is_authenticated() and request.user.is_superuser :
    return _add_user(request, False, False , True, False)
    #else:
        #raise PermissionDenied()


@api_view(['POST','GET'])
def register_parents(request):
   return _add_user(request, True, False , False , False)


@api_view(['POST','GET'])
def register_psychology(request):
   return _add_user(request, False, True , False , False)



@api_view(['POST','GET'])
def register_helper(request):
   return _add_user(request, False, False , False , True)


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
        return False





def belong_FileNumber_Psy_activate(user,file_number):
    if is_member(user,'Psychology'):
        file_number=int(file_number)
        queryset=request_consultant.objects.filter(user_psy=user, file_number=file_number  ,activ_req=2)
        if queryset.exists():
            return True
        else:
            return False
    else:
        return False


def belong_FileNumber_helper(user,file_number):
    if is_member(user,'Helper'):
        file_number=int(file_number)
        queryset=Helper_file_number.objects.filter(Helper=user,file_number=file_number)
        if queryset.exists():
            return True
        else:
            return False
    return False





def Check_Permissions_Request_User(user,file_number,txt_permission):
    txt_permission='Farzand_Parvari_app.'+txt_permission
    if belong_FileNumber_User(user,file_number)  :
        return True
    elif belong_FileNumber_helper(user,file_number) or belong_FileNumber_Psy(user, file_number):
        if Check_Permission_groups(user,txt_permission) or txt_permission=='Farzand_Parvari_app.List' :
            return True
        else:
            return False
    else:
        return False

#________________add role helper
@csrf_exempt
@api_view(['POST'])
def active_role_helper(request):
    if request.user.is_authenticated():
        if request.method=='POST':
            located=located_user_groups(request.user,'Helper')
            return JsonResponse({'message':'Active Role of Helper'}, status=200)
        else:
            return JsonResponse({'massage':'method request must be POST'} , status=405)
    else:
        return JsonResponse({'massage':'user is not authenticated'} , status=405)
#______________________________Render HTML page

@login_required
def render_html_profile_parents(request):
    query = Profile_Parents.objects.filter(user = request.user)
    if request.user.is_authenticated() and is_member(request.user , 'Parents') and query.exists():
        return render(request, 'profile_parents.html' , {'profile':query.get()} )
    elif request.user.is_authenticated() and is_member(request.user, 'Parents') and not (query.exists()):
        return render(request, 'profile_parents.html', {'profile': None,})
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')


@login_required
def render_html_profile_psychology(request):
    query = ProfilePsy.objects.filter(user=request.user)
    if request.user.is_authenticated() and is_member(request.user , 'Psychology') and query.exists():
        return render(request, 'profile_psy.html' , {'profile':query.get()} )
    elif request.user.is_authenticated() and is_member(request.user, 'Psychology') and not (query.exists()):
        return render(request, 'profile_psy.html', {'profile': None,})
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')


@login_required
def render_html_List_create_children(request):
    obj = Children.objects.filter(Parent=request.user)
    if request.user.is_authenticated() and is_member(request.user , 'Parents') and obj.exists():
        return render(request, 'List_Create_Children.html' , {'childrens':obj.all()} )
    elif request.user.is_authenticated() and is_member(request.user, 'Parents') and not (obj.exists()):
        return render(request, 'List_Create_Children.html', {'childrens': None,})
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')

@login_required
def render_html_List_update_children(request ,file_number):
    obj = Children.objects.filter(Parent=request.user , file_number=file_number)
    if request.user.is_authenticated() and is_member(request.user , 'Parents') and obj.exists():
        return render(request, 'List_Update_Children.html' , {'child':obj.get()} )
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')

@login_required
def render_select_file_number(request ,file_number):
    if  is_member(request.user, 'Parents') or is_member(request.user, 'Psychology') or is_member(request.user,'Helper'):
        obj = Steps_training.objects.all();
        file_number_auth = Children.objects.filter(Parent=request.user , file_number= file_number)
        request_auth = request_consultant.objects.filter(user_psy= request.user , file_number__file_number=file_number)
        helper_auth = Helper_file_number.objects.filter(Helper= request.user , file_number__file_number=file_number)
        if file_number_auth.exists() or request_auth.exists() or helper_auth :
            if obj.exists():
                obj_all_psy = ProfilePsy.objects.all()
                #massage_data = views_chat_online.get_chat_fun()
                #chat_messages = massage_data[0]
                #first_message_id = massage_data[1]
                helper_obj = User.objects.filter(groups__name='Helper').all();
                file_number_obj = Children.objects.filter(file_number= file_number)
                Agenda_obj= Agenda_fileNumber.objects.filter(file_number__file_number=file_number)
                return render(request, 'file_number.html' , {
                                            'step_training':obj ,
                                            'file_number':file_number_obj.get() ,
                                            'obj_all_psy':obj_all_psy,
                                            #'chat_messages':chat_messages ,
                                            #'first_message_id':first_message_id,
                                            'chat_messages': None,
                                            'first_message_id':None,
                                            'helper_obj':helper_obj,
                                            'Agenda_obj':Agenda_obj,
                                        } )

            else:
                raise FileNotFoundError('آموزش برای این قسمت را در نظر گرفته نشده است')
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')

@login_required
def render_answer_Exercise(request ,file_number,exercise_id):
    obj_child= Children.objects.get(file_number=file_number)
    obj_Exercise = Steps_exercise.objects.get(id=exercise_id)
    obj_answer = Answer_Exercise.objects.filter(file_number=obj_child ,Exercise = obj_Exercise)
    if obj_answer.exists() and request.user.is_authenticated() and belong_FileNumber_User(request.user,file_number):
        return render(request,'answer_Exercise.html',  {'answer':obj_answer.get(), 'obj_file_number':obj_child , 'obj_exercise':obj_Exercise , } )
    elif not obj_answer.exists() and request.user.is_authenticated() and belong_FileNumber_User(request.user,file_number):
        return render(request, 'answer_Exercise.html', {'answer':None,'obj_file_number': obj_child , 'obj_exercise':obj_Exercise , } )
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')

@login_required
def render_comments_training(request ,file_number,step_id):
    obj_steps = Steps_training.objects.get(id=step_id)
    obj_child = Children.objects.get(file_number=file_number)
    obj_comments = Comments_FileNumber_Training.objects.filter(file_number=obj_child , Steps=obj_steps)
    if obj_comments.exists() and request.user.is_authenticated() and belong_FileNumber_User(request.user,file_number):
        return render(request,'comments_training.html',  {'obj_comments':obj_comments.get(), 'obj_file_number':obj_child , 'obj_training':obj_steps , } )
    elif not obj_comments.exists() and request.user.is_authenticated() and belong_FileNumber_User(request.user,file_number):
        return render(request, 'comments_training.html', {'obj_comments':None, 'obj_file_number':obj_child , 'obj_training':obj_steps , } )
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')

@login_required
# when create behavior , id_behavior equal 0
# when create behavior , id_behavior equal id of behavior selected
def render_create_update_behavior(request ,file_number,id_behavior):
    if request.user.is_authenticated() and belong_FileNumber_User(request.user, file_number):
        file_number = Children.objects.get(file_number=file_number)
        if id_behavior:
            return render(request, 'behavior_update_create.html', )
        else:
            return render(request, 'behavior_update_create.html',)

    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')
@login_required
def render_behavior_html(request ,file_number,behavior_id):
    if request.user.is_authenticated():
        if belong_FileNumber_User(request.user ,file_number) or belong_FileNumber_Psy(request.user ,file_number) or belong_FileNumber_helper(request.user ,file_number):
            file_number_obj = Children.objects.filter(file_number=file_number)
            behavior_obj = Children_behavior.objects.filter(id=behavior_id , file_number=file_number_obj)

            if  file_number_obj.exists() and behavior_obj.exists():

                descript_behavior_obj = Descript_behavior.objects.filter(Behavior=behavior_obj)
                record_behavior_Weekly_obj = record_behavior_Weekly.objects.filter(behavior=behavior_obj)
                Cause_list_admin_obj = Cause_list.objects.all()
                Cause_file_number_obj = Cause_file_number.objects.filter(behavior=behavior_obj).all()
                type_of_Rewrard_obj = type_of_Rewrard.objects.all()
                Rewards_behavior_obj = Rewards_behavior.objects.filter(behavior=behavior_obj).all()
                Rules_behavior_obj = Rules_Reward.objects.filter(behavior=behavior_obj).all()
                Star_table_obj = Star_Table.objects.filter(behavior=behavior_obj).all()
                Punishment_behavior_obj = Punishment_behavior.objects.filter(behavior=behavior_obj).all()
                Situation_defficult_behavior_obj = Situation_defficult_behavior.objects.filter(behavior=behavior_obj).all()
                Suprice_table_obj = Surprice_Table.objects.filter(behavior=behavior_obj).all()

                return render(request, 'behavior.html',
                              {'file_number_obj': file_number_obj.get(),
                               'behavior_obj': behavior_obj.get(),
                               'descript_behavior_obj':descript_behavior_obj.all(),
                               'record_behavior_Weekly_obj' : record_behavior_Weekly_obj,
                               'Cause_list_admin_obj':Cause_list_admin_obj,
                               'Cause_file_number_obj':Cause_file_number_obj,
                               'type_of_Rewrard_obj': type_of_Rewrard_obj,
                               'Rewards_behavior_obj':Rewards_behavior_obj,
                               'Rules_behavior_obj' : Rules_behavior_obj,
                               'Star_table_obj' : Star_table_obj,
                               'Punishment_behavior_obj' : Punishment_behavior_obj,
                               'Situation_defficult_behavior_obj':Situation_defficult_behavior_obj,
                               'Suprice_table_obj':Suprice_table_obj,
                               })
            else:
                raise ValidationError('شماره پرونده و رفتار انتخاب شده صحیح نمی باشد');
    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')


# render update Descrption of behaviors (Step one)
@login_required
def render_Update_descript_behaviors_step_1(request ,file_number,behavior_id,descript_id):
    file_number_obj = Children.objects.filter(Parent=request.user, file_number=file_number)
    behavior_obj = Children_behavior.objects.filter(id=behavior_id, file_number=file_number_obj)
    descript_behavior_obj = Descript_behavior.objects.filter(Behavior=behavior_obj, id = descript_id)

    if descript_behavior_obj.exists() and request.user.is_authenticated() and belong_FileNumber_User(request.user,file_number):
        return render(request,'Update_descript_behaviors_step_1.html',
                      {
                          'file_number_obj':file_number_obj.get(),
                          'behavior_obj':behavior_obj.get(),
                          'descript_behavior_obj':descript_behavior_obj.get(),
                      })

    elif not belong_FileNumber_User(request.user,file_number):
        raise PermissionError('شما دسترسی به این صفحه را ندارید')
    else:
        raise ValidationError('مقادیر صحیح نمی باشد')

 #_________________________________________Render psycology
@login_required
def render_psy(request):
    if request.user.is_authenticated() and is_member(request.user,'Psychology') :
        new_request_obj = request_consultant.objects.filter(user_psy=request.user , activ_req=1 ).all()
        active_request_obj = request_consultant.objects.filter(user_psy=request.user, activ_req=2).all()
        #massage_data = views_chat_online.get_chat_fun()
        #chat_messages = massage_data[0]
        #first_message_id = massage_data[1]
        general_noting_obj= general_noting.objects.filter(consultant= request.user)
        return render(request, 'psy.html', {
            'new_request_obj':new_request_obj,
            'active_request_obj':active_request_obj,
            #'chat_messages':chat_messages,
            #'first_message_id':first_message_id,
            'chat_messages': None,
            'first_message_id':None,
            'general_noting_obj':general_noting_obj,
        })

    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')



@login_required
def render_cost_time(request , id_request):
    psy_request_obj = request_consultant.objects.filter(user_psy=request.user,id=id_request)
    parent_request_obj = request_consultant.objects.filter(id=id_request, user_request=request.user)
    if psy_request_obj.exists() or parent_request_obj.exists():
        request_obj = request_consultant.objects.filter(id=id_request).get()
        set_time_obj = Set_Time_Cost_filenumber.objects.filter(request__id=id_request)
        if set_time_obj.exists():
                set_time_obj_get = set_time_obj.get()

        else:
            set_time_obj_get=None
        return  render(request,'Cost_Time_Psy.html' , {
                            "set_time_obj" :set_time_obj_get,
                            "request_obj": request_obj
                       })
    else:
        raise PermissionError('دسترسی به این صفحه ندارید')

@login_required
def render_agenda_file_number(request,file_number):
    if belong_FileNumber_Psy(request.user, file_number)  :
       active_request_obj = request_consultant.objects.filter(user_psy=request.user, activ_req=2 , file_number__file_number=file_number)
       if active_request_obj.exists():
           Agenda_fileNumber_obj = Agenda_fileNumber.objects.filter(user_psy=request.user,file_number__file_number=file_number)
           file_number_obj = Children.objects.filter(file_number=file_number)
           return render(request,'Agenda_file_number.html',{
               'Agenda_fileNumber_obj':Agenda_fileNumber_obj.all(),
               'file_number_obj':file_number_obj.get(),

                })
       else:
           raise ValidationError('درخواست پرونده فعال نشده است لطفا درخواست پرونده را فعال کنید')
    else:
        raise PermissionError('دسترسی به این صفحه ندارید')

@login_required
def render_noting_file_number(request,file_number):
    if belong_FileNumber_Psy(request.user, file_number)  :
       active_request_obj = request_consultant.objects.filter(user_psy=request.user, activ_req=2 , file_number__file_number=file_number)
       if active_request_obj.exists():
           notting_fileNumber_obj = notting_fileNumber.objects.filter(file_number__file_number=file_number, consultant = request.user)
           file_number_obj = Children.objects.filter(file_number=file_number)
           return render(request,'Noting_file_number.html',{
               'notting_fileNumber_obj':notting_fileNumber_obj,
               'file_number_obj':file_number_obj.get(),

                })
       else:
           raise ValidationError('درخواست پرونده فعال نشده است لطفا درخواست پرونده را فعال کنید')
    else:
        raise PermissionError('دسترسی به این صفحه ندارید')



@login_required
def render_helper(request):
    if request.user.is_authenticated() and is_member(request.user , 'Helper'):
        Helper_file_number_obj = Helper_file_number.objects.filter(Helper=request.user)
        massage_data = views_chat_online.get_chat_fun()
        chat_messages = massage_data[0]
        first_message_id = massage_data[1]
        return render(request, 'helper.html', {
                'Helper_file_number_obj':Helper_file_number_obj.all(),
                'chat_messages':chat_messages,
                'first_message_id':first_message_id
            })

    else:
        raise PermissionError('شما دسترسی به این صفحه را ندارید')