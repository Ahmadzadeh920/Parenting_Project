from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User,Permission,Group
from datetime import datetime
import requests
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import APIException,PermissionDenied,ValidationError
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from .models import (Profile_Parents,
                     Profile_Psy,
                    Children,
                    Steps_exercise,
                    Steps_training,
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
                    Surprice_Table,
                    Star_Table,
                    Punishment_behavior,
                    Situation_defficult_behavior,
                    request_consultant,
                    Agenda_fileNumber,

                     )
import Farzand_Parvari_app.views as views
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from .Serializer import (User_serialize,
                        Profile_Parents_serialize,
                        Profile_psy_serilalize,
                        Children_serilalize,
                        Steps_excercise_serialize,
                        Steps_training_serialize,
                        Answer_Exercise_serialize,
                        List_Answer_Exercise_serialize,
                        Comments_FileNumber_serialize,
                        Chidren_behavior_list_serialize,
                        Chidren_behavior_Update_Retrive_Create_serialize,
                        Descript_behavior_serialize,
                        record_behavior_Weekly_serialize,
                        Cause_list_serialize,
                        Cause_file_number_serialize,
                        Rewards_serialize,
                        Type_Rewards_serialize,
                        Reward_behavior_serialize,
                        Rules_Reward_serialize,
                        List_Table_star_serialize,
                        Create_Table_star_serialize,
                        Create_Table_surprise_serialize,
                        List_Table_surprise_serialize,
                        List_Punishment_recommend_serialize,
                        Punishment_behavior_serialize,
                        Situation_defficult_behavior_serialize,
                        List_psy_serilalize,
                        Create_Request_psy_serialize,
                        List_Request_psy_serialize,
                        Create_Agenda_serialize,
                        List_Agenda_serialize,
                        Retrieve_Agenda_serialize,
                        List_new_request_serialize,
                        View_file_number_consultant_serialize,
                        List_behavior_consultant_serialize,
                        change_StausRequest_consultant_serialize,
                        Set_time_cost_filenumber_serialize,
                        Create_question_psy_serialize,
                        Update_answer_parent_serialize,
                        List_ongoing_consultant_serialize,
                        noting_fileNumber_serialize,
                        general_noting_serialize
                        )
# Create your views here.

class TestAuthView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        return Response("Hello {0}!".format(request.user))

# log out Class via rest_auth
class LogoutViewEx(LogoutView):
    authentication_classes = (authentication.TokenAuthentication,)
# Complete Profile Parents
class Profile_Parents_view(generics.CreateAPIView):
    serializer_class=Profile_Parents_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        if Profile_Parents.objects.filter(user=self.request.user).exists():
            if views.is_member(self.request.user,'Parents'):
                queryset=Profile_Parents.objects.get(user=self.request.user)
            else:
                raise PermissionDenied
        queryset=None

    def perform_create(self, serializer):
        queryset = Profile_Parents.objects.filter(user=self.request.user)
        if queryset.exists():
            return self.get_queryset()
        else:
            if views.is_member(self.request.user,'Parents'):
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied

class Profile_Psychology_view(generics.CreateAPIView):
    serializer_class=Profile_psy_serilalize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        if Profile_Psy.objects.filter(user=self.request.user).exists():
            if views.is_member(self.request.user, 'Psychology'):
                queryset=Profile_Psy.objects.get(user=self.request.user)
            else:
                raise PermissionDenied
        else:
            queryset=None
        return queryset

    def perform_create(self, serializer):
        queryset = Profile_Psy.objects.filter(user=self.request.user)
        if queryset.exists():
            return self.get_queryset()
        else:
            if views.is_member(self.request.user, 'Psychology'):
                if views.validate_file_size(self.request.data['profile_image_psy']):
                    serializer.save(user=self.request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied


# RetriveUpdae Prifile of Parents
class Retrive_Update_Profile_Parents(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Profile_Parents_serialize
    lookup_field ='user'
    def get_object(self):
        user = self.request.user
        if views.is_member(user,'Parents'):
            return get_object_or_404(Profile_Parents, user=user)
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
           raise PermissionDenied
## RetriveUpdae Prifile of Psychology
class Retrive_Update_Profile_Psy(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Profile_psy_serilalize
    lookup_field ='user'
    def get_object(self):
        user = self.request.user
        if views.is_member(user,'Psychology'):
            return get_object_or_404(Profile_Psy, user=user)
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise PermissionDenied

#_________________________________________________Chidren _____________

# For Create Profile of Chidren
class Children_Create(generics.CreateAPIView):
    serializer_class=Children_serilalize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        if Children.objects.filter(parent=self.request.user).exists():
            queryset=Children.objects.get(user=self.request.user)
        queryset=None

    def perform_create(self, serializer):
        queryset = Children.objects.filter(Parent=self.request.user)
        if views.is_member(self.request.user,'Parents'):
            date=datetime.now()
            serializer.save(Parent=self.request.user,Date_create=date)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied



#List
class Children_List(generics.ListAPIView):
    serializer_class = Children_serilalize
    model = Children_serilalize.Meta.model
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        Parent = self.request.user
        if views.is_member(Parent,'Parents'):
            queryset = self.model.objects.filter(Parent=Parent)
            return queryset.order_by('file_number')
        else:
            PermissionDenied
#Update and Retrive Children

class Children_Update(generics.RetrieveUpdateAPIView):
    serializer_class = Children_serilalize
    model = Children_serilalize.Meta.model
    permission_classes = (permissions.IsAuthenticated,)

    lookup_field = 'file_number'

    def get_object(self):
        file_number = int(self.kwargs['file_number'])
        parent=self.request.user
        if views.is_member(parent, 'Parents'):
            return get_object_or_404(Children, file_number=file_number, Parent=parent)
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
           raise PermissionDenied

#________________________________________________________Training
# List Steps of Training:
class Steps_Training_List(generics.ListAPIView):
    serializer_class = Steps_training_serialize
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Steps_training.objects.all()

# List Steps of Execise:
class Steps_Exercise_List(generics.ListAPIView):
    serializer_class = Steps_excercise_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = Steps_exercise

    def get_queryset(self):
        training_id= self.kwargs['training_id']
        steps=Steps_training.objects.filter(id=training_id).exists()
        if steps:
            queryset = self.model.objects.filter(steps=steps)
            return queryset.order_by('id')
        else:
            raise ValidationError



#  Comments on steps of Training
# Create
class Create_Comments_steps(generics.CreateAPIView):
    serializer_class = Comments_FileNumber_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        steps_id=int(self.kwargs['step_id'])
        file_number=self.kwargs['file_number']
        if views.belong_FileNumber_User(self.request.user,file_number):
            Step_obj=Steps_training.objects.filter(id=steps_id)
            file_number_obj=Children.objects.filter(file_number=file_number)
            if Step_obj and file_number_obj:
                if Comments_FileNumber_Training.objects.filter(Steps=Step_obj,file_number=file_number_obj).exists():
                    queryset = Comments_FileNumber_Training.objects.get(Steps=Step_obj,file_number=file_number_obj)
                    return queryset
                return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        if queryset:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
             steps_id = int(self.kwargs['step_id'])
             file_number = int(self.kwargs['file_number'])
             Step_obj = Steps_training.objects.get(id=steps_id)
             file_number_obj = Children.objects.get(file_number=file_number)
             serializer.save(Steps=Step_obj,file_number=file_number_obj)
             return Response(serializer.data, status=status.HTTP_201_CREATED)

# Update and Retrive
class Update_Retrive_Comments_steps(generics.RetrieveUpdateAPIView):
    serializer_class = Comments_FileNumber_serialize
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field ='file_number'
    def get_object(self):
        steps_id=int(self.kwargs['step_id'])
        file_number=self.kwargs['file_number']
        if views.belong_FileNumber_User(self.request.user,file_number):
            Step_obj=Steps_training.objects.get(id=steps_id)
            file_number_obj=Children.objects.get(file_number=file_number)
            if Step_obj and file_number_obj:
                if Comments_FileNumber_Training.objects.filter(Steps=Step_obj,file_number=file_number_obj).exists():
                    queryset = Comments_FileNumber_Training.objects.get(Steps=Step_obj,file_number=file_number_obj)
                    return queryset
                return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
           self.get_queryset()


#___________________________________Answer To_Exercise

class Create_Answer_Exercise(generics.CreateAPIView):
    serializer_class = Answer_Exercise_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        exer_id=int(self.kwargs['exercise_id'])
        file_number=self.kwargs['file_number']
        if views.belong_FileNumber_User(self.request.user,file_number):
            Exercise_obj=Steps_exercise.objects.filter(id=exer_id)
            file_number_obj=Children.objects.filter(file_number=file_number)
            if Exercise_obj and file_number_obj:
                if Answer_Exercise.objects.filter(Exercise=Exercise_obj,file_number=file_number_obj).exists():
                    queryset = Answer_Exercise.objects.get(Exercise=Exercise_obj,file_number=file_number_obj)
                    return queryset
                return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        if queryset:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            exer_id = int(self.kwargs['exercise_id'])
            file_number = self.kwargs['file_number']
            Exercise_obj = Steps_exercise.objects.get(id=exer_id)
            file_number_obj = Children.objects.get(file_number=file_number)
            serializer.save(Exercise=Exercise_obj,file_number=file_number_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# Update and Retrive
class Update_Retrive_Answer_Exercise(generics.RetrieveUpdateAPIView):
    serializer_class = Answer_Exercise_serialize
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field ='file_number'
    def get_object(self):
        exer_id=int(self.kwargs['exercise_id'])
        file_number=self.kwargs['file_number']
        if views.belong_FileNumber_User(self.request.user,file_number):
            Exercise_obj=Steps_exercise.objects.filter(id=exer_id)
            file_number_obj=Children.objects.filter(file_number=file_number)
            if Exercise_obj and file_number_obj:
                if Answer_Exercise.objects.filter(Exercise=Exercise_obj,file_number=file_number_obj).exists():
                    queryset = Answer_Exercise.objects.get(Exercise=Exercise_obj,file_number=file_number_obj)
                    return queryset
                return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

class List_answer_exer(generics.ListAPIView):
    serializer_class = List_Answer_Exercise_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        if Children.objects.filter(file_number=file_number).exists():
            file_number_obj=Children.objects.get(file_number=file_number)
            if views.Check_Permissions_Request_User(self.request.user,file_number,'List'):
                queryset = self.model.objects.filter(file_number=file_number_obj)
                return queryset
            else:
                raise PermissionDenied
        raise ValidationError




#_______________________________________ Crete Behaviors

# Create Behavior
class Create_bahavior(generics.CreateAPIView):
    serializer_class = Chidren_behavior_Update_Retrive_Create_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        if views.belong_FileNumber_User(self.request.user,file_number):
            file_number_obj=Children.objects.filter(file_number=file_number)
            if  file_number_obj:
                queryset=Children_behavior.objects.filter(user=self.request.user,file_number=file_number_obj).all()
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        name_behavior= self.request.data['Behavior_name']
        file_number_obj = Children.objects.get(file_number=file_number)
        if Children_behavior.objects.filter(Behavior_name=name_behavior, file_number=file_number_obj).exists():
            return Response(queryset, status=status.HTTP_409_CONFLICT)
        else:
            serializer.save(user=self.request.user,file_number=file_number_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# List all of the bahavior which is belong to file_number

class List_bahavior(generics.ListAPIView):
    serializer_class = Chidren_behavior_list_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        if Children.objects.filter(file_number=file_number).exists():
            file_number_obj=Children.objects.get(file_number=file_number)
            if views.Check_Permissions_Request_User(self.request.user,file_number,'List'):
                queryset = self.model.objects.filter(file_number=file_number_obj)
                return queryset
            else:
                raise PermissionDenied
        raise ValidationError





#Update and Retrieve

class Update_Retrive_Behavior(generics.RetrieveUpdateAPIView):
    serializer_class = Chidren_behavior_Update_Retrive_Create_serialize
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field ='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior=int(self.kwargs['id_behavior'])
        if views.belong_FileNumber_User(self.request.user, file_number):
            file_number_obj = Children.objects.filter(file_number=file_number)
            if file_number_obj:
               if Children_behavior.objects.filter(user=self.request.user,file_number=file_number_obj ,id = id_bahavior).exists():
                   queryset=Children_behavior.objects.get(user=self.request.user,file_number=file_number_obj,id = id_bahavior)
                   return queryset
               else:
                   return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

# ----------------------------------
# Create Description of Behaviors
class Create_descriptions(generics.CreateAPIView):
    serializer_class = Descript_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_descript_behavior'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Descript_behavior.objects.filter(Behavior=behavior_obj).exists():
                    queryset=Descript_behavior.objects.filter(Behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            serializer.save(Behavior=behavior_obj_get , user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_descripttions(generics.ListAPIView):
    serializer_class = Descript_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        id_bahavior = self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user, file_number, 'List'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
            if behavior_obj.exists():
                if Descript_behavior.objects.filter(Behavior=behavior_obj).exists():
                    queryset = Descript_behavior.objects.filter(Behavior=behavior_obj).all()
                else:
                    queryset = None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_descriptions(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Descript_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field ='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior=int(self.kwargs['behavior_id'])
        id_descript=int(self.kwargs['descript_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number,'change_descript_behavior') or views.Check_Permissions_Request_User(self.request.user, file_number,'delete_descript_behavior'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
            if behavior_obj.exists():
                if Descript_behavior.objects.filter(id=id_descript , Behavior=behavior_obj).exists():
                    queryset = Descript_behavior.objects.get(id=id_descript, Behavior=behavior_obj)
                    return queryset
                else:
                   raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError


#_____________________________record_behavior_Weekly


class Create_record_weekly(generics.CreateAPIView):
    serializer_class = record_behavior_Weekly_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_record_behavior_weekly'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if record_behavior_Weekly.objects.filter(behavior=behavior_obj).exists():
                    queryset=record_behavior_Weekly.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            serializer.save(behavior=behavior_obj_get,user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_Record_Bahavior(generics.ListAPIView):
    serializer_class = record_behavior_Weekly_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        id_bahavior = self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user, file_number, 'List'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            if behavior_obj.exists():
                if record_behavior_Weekly.objects.filter(behavior=behavior_obj).exists():
                    queryset = record_behavior_Weekly.objects.filter(behavior=behavior_obj).all()
                    return queryset
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_record_weekly(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = record_behavior_Weekly_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field ='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior=int(self.kwargs['behavior_id'])
        id_record=int(self.kwargs['record_weekly_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number,'change_record_behavior_weekly') or views.Check_Permissions_Request_User(self.request.user, file_number,'delete_record_behavior_weekly'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(id=id_record , behavior=behavior_obj).exists():
                    queryset = self.model.objects.get(id=id_record , behavior=behavior_obj)
                    return queryset
                else:
                   raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError

#____________________________Step 2

class List_Cause_List(generics.ListAPIView):
    serializer_class = Cause_list_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset=Cause_list.objects.all()
        return queryset


class Create_Cause_file_number(generics.CreateAPIView):
    serializer_class = Cause_file_number_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_cause_file_number'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Cause_file_number.objects.filter(behavior=behavior_obj).exists():
                    queryset=Cause_file_number.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            Cause_obj=Cause_list.objects.get(id=self.request.data['Cause'])
            if Cause_file_number.objects.filter(Cause=Cause_obj,behavior=behavior_obj,user=self.request.user).exists():
                return self.get_queryset()
            else:
                serializer.save(behavior=behavior_obj_get,user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_Cause_file_number(generics.ListAPIView):
    serializer_class = Cause_file_number_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        id_bahavior = self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user, file_number, 'List'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            if behavior_obj.exists():
                if Cause_file_number.objects.filter(behavior=behavior_obj).exists():
                    queryset = Cause_file_number.objects.filter(behavior=behavior_obj).all()
                    return queryset
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_Cause_file_number(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Cause_file_number_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field ='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior=int(self.kwargs['behavior_id'])
        id_Cause_file=int(self.kwargs['Cause_file_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number,'change_cause_file_number') or views.Check_Permissions_Request_User(self.request.user, file_number,'delete_cause_file_number'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(id=id_Cause_file , behavior=behavior_obj).exists():
                    queryset = self.model.objects.get(id=id_Cause_file , behavior=behavior_obj)
                    return queryset
                else:
                   raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError



#___________________
# List all of the rewards which is recommened to User
class List_type_Rewards(generics.ListAPIView):
    serializer_class = Type_Rewards_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset=self.model.objects.all()
        return queryset

class List_Rewards(generics.ListAPIView):
    serializer_class = Rewards_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset=self.model.objects.all()
        return queryset

# manage Rewards of Behaviors

class Create_Rewards_behavior(generics.CreateAPIView):
    serializer_class = Reward_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_rewards_behavior'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj).exists():
                    queryset=Rewards_behavior.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            serializer.save(behavior=behavior_obj_get,user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_Reward_behavior(generics.ListAPIView):
    serializer_class = Reward_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'List'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj).exists():
                    queryset=Rewards_behavior.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_Reward_behavior(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Reward_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field ='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior=int(self.kwargs['behavior_id'])
        id_reward=int(self.kwargs['Reward_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number,'change_rewards_behavior') or views.Check_Permissions_Request_User(self.request.user, file_number,'delete_rewards_behavior'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(id=id_reward , behavior=behavior_obj).exists():
                    queryset = self.model.objects.get(id=id_reward , behavior=behavior_obj)
                    return queryset
                else:
                   raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError


# Rule of Rewards

class Create_Rule_Rewards(generics.CreateAPIView):
    serializer_class = Rules_Reward_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        id_reward=self.kwargs['reward_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_rules_reward'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj,id=id_reward).exists():
                    Reward_obj=Rewards_behavior.objects.get(behavior=behavior_obj,id=id_reward)
                    if Rules_Reward.objects.filter(Reward=Reward_obj).exists():
                        queryset=Rules_Reward.objects.filter(Reward=Reward_obj).all()
                        return queryset
                    else:
                        return None
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        id_reward = self.kwargs['reward_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            if Rewards_behavior.objects.filter(behavior=behavior_obj_get, id=id_reward).exists():
                Reward_obj = Rewards_behavior.objects.get(behavior=behavior_obj_get, id=id_reward)
                serializer.save(Reward=Reward_obj,user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_Rule_Reward(generics.ListAPIView):
    serializer_class = Rules_Reward_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        id_reward=self.kwargs['reward_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'List'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj,id=id_reward).exists():
                    Reward_obj=Rewards_behavior.objects.get(behavior=behavior_obj,id=id_reward)
                    if Rules_Reward.objects.filter(Reward=Reward_obj).exists():
                        queryset=Rules_Reward.objects.filter(Reward=Reward_obj).all()
                        return queryset
                    else:
                        return None
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_Rule_Reward(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Rules_Reward_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field = 'id'

    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        id_reward = int(self.kwargs['reward_id'])
        id_rule=int(self.kwargs['rule_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number,
                                                'change_rules_reward') or views.Check_Permissions_Request_User(
                self.request.user, file_number, 'delete_rules_reward'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            if behavior_obj.exists():
                if behavior_obj.exists():
                    if Rewards_behavior.objects.filter(behavior=behavior_obj, id=id_reward).exists():
                        Reward_obj = Rewards_behavior.objects.get(behavior=behavior_obj, id=id_reward)
                        if Rules_Reward.objects.filter(Reward=Reward_obj, id=id_rule).exists():
                            queryset = self.model.objects.get(Reward=Reward_obj, id=id_rule)
                            return queryset
                        else:
                            return None
                    else:
                        raise ValidationError
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError

#_______________________________________Start Table


class Create_Star_Table(generics.CreateAPIView):
    serializer_class = Create_Table_star_serialize
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        id_reward=self.kwargs['reward_id']
        id_rules=self.kwargs['rule_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_star_table'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj,id=id_reward).exists():
                    Reward_obj=Rewards_behavior.objects.get(behavior=behavior_obj,id=id_reward)
                    if Rules_Reward.objects.filter(Reward=Reward_obj,id=id_rules).exists():
                        Rules_obj=Rules_Reward.objects.get(Reward=Reward_obj, id=id_rules)
                        if Star_Table.objects.filter(reward_rule=Rules_obj).exists():
                            queryset=Star_Table.objects.filter(reward_rule=Rules_obj).all()
                            return queryset
                        else:
                            return None
                    else:
                        raise ValidationError
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        id_reward = self.kwargs['reward_id']
        id_rules = self.kwargs['rule_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            if Rewards_behavior.objects.filter(behavior=behavior_obj_get, id=id_reward).exists():
                Reward_obj = Rewards_behavior.objects.get(behavior=behavior_obj_get, id=id_reward)
                if Rules_Reward.objects.filter(Reward=Reward_obj).exists():
                    Rules_obj = Rules_Reward.objects.get(Reward=Reward_obj, id=id_rules)
                    serializer.save(reward_rule=Rules_obj,user=self.request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise ValidationError
            else:
                raise ValidationError
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_Star_Table(generics.ListAPIView):
    serializer_class = List_Table_star_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        id_reward = self.kwargs['reward_id']
        id_rules = self.kwargs['rule_id']
        if views.Check_Permissions_Request_User(self.request.user, file_number, 'List'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj, id=id_reward).exists():
                    Reward_obj = Rewards_behavior.objects.get(behavior=behavior_obj, id=id_reward)
                    if Rules_Reward.objects.filter(Reward=Reward_obj,id=id_rules).exists():
                        Rules_obj = Rules_Reward.objects.get(Reward=Reward_obj, id=id_rules)
                        if Star_Table.objects.filter(reward_rule=Rules_obj).exists():
                            queryset = Star_Table.objects.filter(reward_rule=Rules_obj).all()
                            return queryset
                        else:
                            return None
                    else:
                        raise ValidationError
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_Table_Star(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = List_Table_star_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field = 'id'
    def get_queryset(self):
        file_number = self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        id_reward = self.kwargs['reward_id']
        id_rules = self.kwargs['rule_id']
        id_star= int(self.kwargs['id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number, 'change_star_table') or views.Check_Permissions_Request_User(self.request.user, file_number, 'delete_star_table'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj, id=id_reward).exists():
                    Reward_obj = Rewards_behavior.objects.get(behavior=behavior_obj, id=id_reward)
                    if Rules_Reward.objects.filter(Reward=Reward_obj, id=id_rules).exists():
                        Rules_obj = Rules_Reward.objects.get(Reward=Reward_obj, id=id_rules)
                        if self.model.objects.filter(reward_rule=Rules_obj, id= id_star).exists():
                            queryset = self.model.objects.filter(reward_rule=Rules_obj, id= id_star).all()
                            return queryset
                        else:
                            return None
                    else:
                        raise ValidationError
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            self.request.data['user'] = self.request.user.id
            self.request.data['reward_rule'] = self.kwargs['rule_id']
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError

#_____________________Surprise Table


class Create_Surprise_Table(generics.CreateAPIView):
    serializer_class = Create_Table_surprise_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        id_reward=self.request.data['Reward']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_surprice_table'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if Rewards_behavior.objects.filter(behavior=behavior_obj,id=id_reward).exists():
                    Reward_obj=Rewards_behavior.objects.get(behavior=behavior_obj,id=id_reward)
                    if self.model.objects.filter(Reward=Reward_obj).exists():
                        queryset=self.model.objects.filter(Reward=Reward_obj).all()
                        return queryset
                    else:
                        return None
                else:
                    raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        if queryset:
            return queryset
        else:
            file_number = int(self.kwargs['file_number'])
            id_bahavior = self.kwargs['behavior_id']
            id_reward = self.request.data['Reward']
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            if behavior_obj.exists():
                behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
                if Rewards_behavior.objects.filter(behavior=behavior_obj_get, id=id_reward).exists():
                    Reward_obj = Rewards_behavior.objects.get(behavior=behavior_obj_get, id=id_reward)
                    serializer.save(user=self.request.user,Date_Time=datetime.now(),Reward=Reward_obj)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise ValidationError
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_surprise_table(generics.ListAPIView):
    serializer_class = List_Table_surprise_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        id_bahavior = int(self.kwargs['behavior_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number, 'add_surprice_table'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(behavior=behavior_obj).exists():
                    queryset = self.model.objects.filter(behavior=behavior_obj).all()
                    return queryset
                else:
                    return None

            else:
                raise ValidationError
        else:
            raise PermissionDenied


##_____________________________________Punishmenr Step 5


class List_punishment_recommend(generics.ListAPIView):
    serializer_class = List_Punishment_recommend_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset=self.model.objects.all()
        return queryset

class Create_Punishment_behavior(generics.CreateAPIView):
    serializer_class =Punishment_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model=Punishment_behavior
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_punishment_behavior'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(behavior=behavior_obj).exists():
                    queryset=self.model.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            serializer.save(behavior=behavior_obj_get,user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_Punishment_behavior(generics.ListAPIView):
    serializer_class = Punishment_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'List'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(behavior=behavior_obj).exists():
                    queryset=self.model.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_Punishment_behavior(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Punishment_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field ='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior=int(self.kwargs['behavior_id'])
        id_punish=int(self.kwargs['Punish_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number,'change_punishment_behavior') or views.Check_Permissions_Request_User(self.request.user, file_number,'delete_punishment_behavior'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(id=id_punish , behavior=behavior_obj).exists():
                    queryset = self.model.objects.get(id=id_punish , behavior=behavior_obj)
                    return queryset
                else:
                   raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            id_bahavior = int(self.kwargs['behavior_id'])
            file_number = self.kwargs['file_number']
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            self.request.data['user']=self.request.user
            self.request.data['behavior'] = behavior_obj
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError


#________________________________Step 6


class Create_Situation_behavior(generics.CreateAPIView):
    serializer_class =Situation_defficult_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model=Situation_defficult_behavior
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'add_situation_defficult_behavior'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(behavior=behavior_obj).exists():
                    queryset=self.model.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        queryset=self.get_queryset()
        file_number = int(self.kwargs['file_number'])
        id_bahavior = self.kwargs['behavior_id']
        behavior_obj=Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
        if behavior_obj.exists():
            behavior_obj_get = Children_behavior.objects.get(id=id_bahavior, file_number=file_number)
            serializer.save(behavior=behavior_obj_get,user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError

# List all of the bahavior which is belong to file_number

class List_Situation_behavior(generics.ListAPIView):
    serializer_class = Situation_defficult_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number=self.kwargs['file_number']
        id_bahavior=self.kwargs['behavior_id']
        if views.Check_Permissions_Request_User(self.request.user,file_number,'List'):
            behavior_obj=Children_behavior.objects.filter(id=id_bahavior ,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(behavior=behavior_obj).exists():
                    queryset=self.model.objects.filter(behavior=behavior_obj).all()
                else:
                    queryset=None
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied
#Update and Retrieve

class Update_Retrive_Situation_behavior(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Situation_defficult_behavior_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field ='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_bahavior=int(self.kwargs['behavior_id'])
        id_situation=int(self.kwargs['situation_id'])
        if views.Check_Permissions_Request_User(self.request.user, file_number,'change_punishment_behavior') or views.Check_Permissions_Request_User(self.request.user, file_number,'delete_punishment_behavior'):
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior,file_number=file_number)
            if behavior_obj.exists():
                if self.model.objects.filter(id=id_situation , behavior=behavior_obj).exists():
                    queryset = self.model.objects.get(id=id_situation , behavior=behavior_obj)
                    return queryset
                else:
                   raise ValidationError
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            id_bahavior = int(self.kwargs['behavior_id'])
            file_number = self.kwargs['file_number']
            behavior_obj = Children_behavior.objects.filter(id=id_bahavior, file_number=file_number)
            self.request.data['user']=self.request.user
            self.request.data['behavior'] = behavior_obj
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError



#________________________________List all of the psychology which is user for request psychology

class List_all_Psy(generics.ListAPIView):
    serializer_class = List_psy_serilalize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    def get_queryset(self):
        queryset=self.model.objects.all()
        return queryset
#____________________________________________Request of psychology
class Create_request_psy(generics.CreateAPIView):
    serializer_class = Create_Request_psy_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model=serializer_class.Meta.model
    def get_queryset(self):
        file_number = self.kwargs['file_number']
        if views.belong_FileNumber_User(self.request.user, file_number):
            file_number_obj = Children.objects.filter(file_number=file_number)
            if file_number_obj.exists():
                queryset = self.model.objects.filter(user_request=self.request.user, file_number=file_number_obj).all()
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        file_number = int(self.kwargs['file_number'])
        queryset=self.get_queryset()
        file_number_obj = Children.objects.get(file_number=file_number)
        psy=self.request.data['user_psy']
        obj_exist=self.model.objects.filter(file_number=file_number_obj, user_psy=psy).exists()
        if obj_exist:
            return self.get_queryset()
        psy_exist=Profile_Psy.objects.filter(user=psy).exists()
        if psy_exist:
            serializer.save(user_request=self.request.user, file_number=file_number_obj ,date_request=datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError


# List all of the bahavior which is belong to file_number

class List_request_psy(generics.ListAPIView):
    serializer_class = List_Request_psy_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model

    def get_queryset(self):
        file_number = self.kwargs['file_number']
        if Children.objects.filter(file_number=file_number).exists():
            file_number_obj = Children.objects.get(file_number=file_number)
            if views.Check_Permissions_Request_User(self.request.user, file_number, 'List'):
                queryset = self.model.objects.filter(file_number=file_number_obj)
                return queryset
            else:
                raise PermissionDenied
        raise ValidationError


# Update and Retrieve

class Update_Retrive_request_psy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Create_Request_psy_serialize
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'
    model=serializer_class.Meta.model
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_request = int(self.kwargs['id_request'])
        if views.belong_FileNumber_User(self.request.user, file_number):
            file_number_obj = Children.objects.filter(file_number=file_number)
            if file_number_obj.exists():
                if self.model.objects.filter(user_request=self.request.user, file_number=file_number_obj,id=id_request).exists():
                    queryset = self.model.objects.get(user_request=self.request.user, file_number=file_number_obj,id=id_request)
                    return queryset
                else:
                    return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            if Profile_Psy.objects.filter(user=self.request.data['user_psy']).exists():
                return self.update(request, *args, **kwargs)
            else:
                raise ValidationError
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError

#_________________________________

class Create_Agenda_File_Number(generics.CreateAPIView):
    serializer_class = Create_Agenda_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model=serializer_class.Meta.model
    def get_queryset(self):
        file_number = self.kwargs['file_number']
        obj_file_number=Children.objects.get(file_number=file_number)
        request_obj=request_consultant.objects.filter(user_psy=self.request.user , file_number=obj_file_number)
        if request_obj.exists() and views.Check_Permissions_Request_User(self.request.user,file_number,'add_agenda_filenumber'):
            obj=self.model.objects.filter(user_psy=self.request.user ,file_number=obj_file_number)
            if obj.exists():
                queryset=obj.all()
                return queryset
            else:
                return None
        else:
            raise PermissionDenied

    def perform_create(self, serializer):
        file_number = int(self.kwargs['file_number'])
        queryset=self.get_queryset()
        file_number_obj = Children.objects.get(file_number=file_number)
        if views.is_member(self.request.user,'Psychology'):
            serializer.save(user_psy=self.request.user,file_number=file_number_obj,date_Agenda=datetime.now())
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied




# List all of the bahavior which is belong to file_number

class List_Agenda(generics.ListAPIView):
    serializer_class = List_Agenda_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    def get_queryset(self):
        file_number = self.kwargs['file_number']
        obj_file_number = Children.objects.get(file_number=file_number)
        request_obj = request_consultant.objects.filter(user_psy=self.request.user, file_number=obj_file_number)
        condition_1=request_obj.exists() and views.Check_Permissions_Request_User(self.request.user, file_number,
                                                                         'List') # check user is psychology
        condition_2=views.belong_FileNumber_User(self.request.user,file_number) # check user is parent
        if condition_1 :
            obj = self.model.objects.filter(user_psy=self.request.user, file_number=obj_file_number)
            if obj.exists():
                queryset = obj.all()
                return queryset
            else:
                return None
        elif condition_2:
            obj = self.model.objects.filter(file_number=obj_file_number)
            if obj.exists():
                queryset = obj.all()
                return queryset
            else:
                return None
        else:
            raise PermissionDenied


# Update and Retrieve

class Update_Retrive_Agenda(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Retrieve_Agenda_serialize
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'
    model=serializer_class.Meta.model
    def get_object(self):
        file_number = self.kwargs['file_number']
        id_agenda = self.kwargs['id_agenda']
        obj_file_number = Children.objects.get(file_number=file_number)
        request_obj = request_consultant.objects.filter(user_psy=self.request.user, file_number=obj_file_number)
        condition_1 =views.Check_Permissions_Request_User(self.request.user, file_number,'change_agenda_filenumber')
        condition_2 = request_obj.exists() and views.Check_Permissions_Request_User(self.request.user, file_number,'delete_agenda_filenumber')
        if condition_1 or condition_2:
            obj = self.model.objects.filter(file_number=obj_file_number , id=id_agenda)
            if obj.exists():
                queryset = self.model.objects.get(file_number=obj_file_number , id=id_agenda)
                return queryset
            else:
                return None
        else:
            raise PermissionDenied


    def put(self, request, *args, **kwargs):
        if self.get_object():
            if views.is_member(self.request.user,'Psychology'):
                #self.request.data['date_Agenda']=datetime.now()
                self.request.data['user_psy'] = self.request.user
                self.request.data['file_number'] = self.kwargs['file_number']
                return self.update(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise ValidationError

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            if views.is_member(self.request.user, 'Psychology'):
                return self.destroy(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise ValidationError
#__________________________________________ Psychology Part
# List new request
class List_new_request(generics.ListAPIView):
    serializer_class = List_new_request_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model =serializer_class.Meta.model
    def get_queryset(self):
        if views.is_member(self.request.user,'Psychology'):
            if self.model.objects.filter(user_psy=self.request.user, activ_req=1).exists():
                queryset=self.model.objects.filter(user_psy=self.request.user, activ_req=1).all()
                return queryset
            else:
                return None
        else:
            raise PermissionDenied


class View_file_number_psy(generics.RetrieveUpdateAPIView):
    serializer_class = View_file_number_consultant_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model =serializer_class.Meta.model
    lookup_field = 'file_number'
    def get_object(self):
        file_number = self.kwargs['file_number']
        if views.belong_FileNumber_Psy(self.request.user, file_number):
            if self.model.objects.filter(file_number=file_number).exists():
                queryset = self.model.objects.get(file_number=file_number)
                return queryset
            else:
                return None

        else:
            raise PermissionDenied

class View_behavior_psy(generics.ListAPIView):
    serializer_class = List_behavior_consultant_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model =serializer_class.Meta.model
    def get_queryset(self):
        file_number = self.kwargs['file_number']
        if views.belong_FileNumber_Psy(self.request.user, file_number):
            if self.model.objects.filter(file_number=file_number).exists():
                queryset = self.model.objects.filter(file_number=file_number).all()
                return queryset
            else:
                return None

        else:
            raise PermissionDenied


class Change_status_request(generics.RetrieveUpdateAPIView):
    serializer_class = change_StausRequest_consultant_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model =serializer_class.Meta.model
    lookup_field = 'id'
    def get_object(self):
        id_request = self.kwargs['id_request']
        if self.model.objects.filter(id=id_request,user_psy=self.request.user  ).exists():
            queryset = self.model.objects.get(id=id_request,user_psy=self.request.user,)
            return queryset
        else:
            return None

    def put(self, request, *args, **kwargs):
        queryset=self.get_object()
        if queryset :
            if 'activ_req' in self.request.data:
                if self.request.data['activ_req']==2:
                    self.request.data['date_active'] = datetime.now()
                else:
                    self.request.data['date_active'] = None
                return self.update(request, *args, **kwargs)
            else:
                raise APIException('request.data missing key activ_req')
        else:
            raise ValidationError

#__________________________________________

class List_Create_time_cost(generics.ListCreateAPIView):
    serializer_class = Set_time_cost_filenumber_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    def get_queryset(self):
        id_request = self.kwargs['id_request']
        if views.is_member(self.request.user,'Psychology') or views.is_member(self.request.user,'Parents'):
            if request_consultant.objects.filter(id=id_request, activ_req=1).exists():
                request_obj=request_consultant.objects.get(id=id_request , activ_req=1)
                if self.model.objects.filter(request=request_obj).exists():
                    queryset=self.model.objects.filter(request=request_obj).all()
                    return queryset
                else:
                    return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied
    def perform_create(self, serializer):
        queryset = self.get_queryset()
        if queryset:
            return queryset
        else:
            id_request = self.kwargs['id_request']
            if views.is_member(self.request.user, 'Psychology'):
                if request_consultant.objects.filter(id=id_request, user_psy=self.request.user, activ_req=1).exists():
                    request_obj = request_consultant.objects.get(id=id_request, user_psy=self.request.user, activ_req=1)
                    serializer.save(request=request_obj)
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    raise ValidationError
            else:
                raise PermissionDenied


#Update and retrieve of set_time_cost_request

class Retrieve_update_time_cost(generics.RetrieveUpdateAPIView):
    serializer_class = Set_time_cost_filenumber_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field='request_id'
    def get_queryset(self):
        id_request = self.kwargs['request_id']
        if views.is_member(self.request.user,'Psychology') or views.is_member(self.request.user,'Parents'):
            if request_consultant.objects.filter(id=id_request, activ_req=1).exists():
                request_obj=request_consultant.objects.get(id=id_request , activ_req=1)
                if self.model.objects.filter(request=request_obj).exists():
                    queryset=self.model.objects.filter(request=request_obj).all()
                    return queryset
                else:
                    return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            id_request = self.kwargs['request_id']
            if views.is_member(self.request.user, 'Psychology'):
                return self.update(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise ValidationError
#_________________________________________________Question_Answer_Request
class List_Create_question_request(generics.ListCreateAPIView):
    serializer_class = Create_question_psy_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    def get_queryset(self):
        id_request = self.kwargs['id_request']
        if views.is_member(self.request.user,'Psychology') or views.is_member(self.request.user,'Parents'):
            if request_consultant.objects.filter(id=id_request, activ_req=1).exists():
                request_obj=request_consultant.objects.get(id=id_request , activ_req=1)
                if self.model.objects.filter(request=request_obj).exists():
                    queryset=self.model.objects.filter(request=request_obj).all()
                    return queryset
                else:
                    return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied
    def perform_create(self, serializer):
        queryset = self.get_queryset()
        id_request = self.kwargs['id_request']
        if views.is_member(self.request.user, 'Psychology'):
            if request_consultant.objects.filter(id=id_request, user_psy=self.request.user, activ_req=1).exists():
                request_obj = request_consultant.objects.get(id=id_request, user_psy=self.request.user, activ_req=1)
                serializer.save(request=request_obj)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                raise ValidationError
        else:
            raise PermissionDenied

class Update_Retrieve_Answer_request(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = Update_answer_parent_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_field='id'
    def get_queryset(self):
        id_request = self.kwargs['id_request']
        id = self.kwargs['id']
        if views.is_member(self.request.user,'Psychology') or views.is_member(self.request.user,'Parents'):
            if request_consultant.objects.filter(id=id_request, activ_req=1).exists():
                request_obj=request_consultant.objects.get(id=id_request , activ_req=1)
                if self.model.objects.filter(request=request_obj , id=id).exists():
                    queryset=self.model.objects.filter(request=request_obj, id=id).all()
                    return queryset
                else:
                    return None
            else:
                raise ValidationError
        else:
            raise PermissionDenied
    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError

#________________________________Ongoing consultations

class List_ongoing_request(generics.ListAPIView):
    serializer_class = List_ongoing_consultant_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model =serializer_class.Meta.model
    def get_queryset(self):
        if views.is_member(self.request.user,'Psychology'):
            if self.model.objects.filter(user_psy=self.request.user, activ_req=2).exists():
                queryset=self.model.objects.filter(user_psy=self.request.user, activ_req=2).all()
                return queryset
            else:
                return None
        else:
            raise PermissionDenied

#______________________Noting_fileNumber
class List_Create_noting_fileNumber(generics.ListCreateAPIView):
    serializer_class = noting_fileNumber_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    def get_queryset(self):
        file_number=self.kwargs['file_number']
        if views.is_member(self.request.user,'Psychology') and views.belong_FileNumber_Psy_activate(self.request.user,file_number):
            if self.model.objects.filter(consultant=self.request.user,file_number=file_number).exists():
                queryset=self.model.objects.filter(consultant=self.request.user,file_number=file_number).all()
                return queryset
            else:
                return None
        else:
            raise PermissionDenied


    def perform_create(self, serializer):
        file_number = self.kwargs['file_number']
        if views.is_member(self.request.user, 'Psychology') and views.belong_FileNumber_Psy_activate(self.request.user,file_number):
            children_obj=Children.objects.get(file_number=int(file_number))
            serializer.save(consultant=self.request.user,file_number=children_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied


class Retrieve_update_noting_file_number(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = noting_fileNumber_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_fields='id'
    def get_object(self):
        file_number = self.kwargs['file_number']
        id = self.kwargs['id']
        if views.is_member(self.request.user, 'Psychology') and views.belong_FileNumber_Psy_activate(self.request.user,                                                                                         file_number):
            if self.model.objects.filter(consultant=self.request.user, file_number=file_number , id=id).exists():
                queryset = self.model.objects.get(consultant=self.request.user, file_number=file_number ,id=id)
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            file_number=self.kwargs['file_number']
            self.request.data['consultant']=self.request.user
            children_obj=Children.objects.get(file_number=file_number)
            self.request.data['file_number'] = children_obj
            return self.update(request, *args, **kwargs)
        else:
           raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError

#________________________________________General noting

class List_Create_general_noting(generics.ListCreateAPIView):
    serializer_class = general_noting_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    def get_queryset(self):
        if views.is_member(self.request.user,'Psychology'):
            if self.model.objects.filter(consultant=self.request.user).exists():
                queryset=self.model.objects.filter(consultant=self.request.user).all()
                return queryset
            else:
                return None
        else:
            raise PermissionDenied


    def perform_create(self, serializer):
        if views.is_member(self.request.user, 'Psychology'):
            serializer.save(consultant=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied


class Retrieve_update_general_noting(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = general_noting_serialize
    permission_classes = (permissions.IsAuthenticated,)
    model = serializer_class.Meta.model
    lookup_fields='id'
    def get_object(self):
        id = self.kwargs['id']
        if views.is_member(self.request.user, 'Psychology'):
            if self.model.objects.filter(consultant=self.request.user, id=id).exists():
                queryset = self.model.objects.get(consultant=self.request.user,id=id)
                return queryset
            else:
                raise ValidationError
        else:
            raise PermissionDenied

    def put(self, request, *args, **kwargs):
        if self.get_object():
            self.request.data['consultant']=self.request.user
            return self.update(request, *args, **kwargs)
        else:
           raise PermissionDenied

    def delete(self, request, *args, **kwargs):
        if self.get_object():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError

