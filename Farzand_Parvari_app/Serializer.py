from rest_framework import serializers
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .models import (Profile_Parents,
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
# User serialize
class User_serialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Password Serilizers
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm
    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        ###### FILTER YOUR USER MODEL ######
        if not User.objects.filter(email=value).exists():

            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            ###### USE YOUR HTML FILE ######
            'html_email_template_name': 'registration\password_reset.html',
            'request': request,
        }
        self.reset_form.save(**opts)


#Profile of Parents Serialize
class Profile_Parents_serialize(serializers.ModelSerializer):
    class Meta:
        model = Profile_Parents
        exclude = ('user',)

class Profile_psy_serilalize(serializers.ModelSerializer):
    psychology = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model =ProfilePsy
        exclude = ('user',)


class List_psy_serilalize(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name =serializers.ReadOnlyField(source='user.last_name')
    class Meta:
        model =ProfilePsy
        fields='__all__'



#___________________________________________


class Children_serilalize(serializers.ModelSerializer):
    psychology = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model =Children
        exclude=('Parent','Date_create')

class Steps_training_serialize (serializers.ModelSerializer):
    class Meta:
        model =Steps_training
        fields = '__all__'

class Steps_excercise_serialize(serializers.ModelSerializer):
    class Meta:
        model =Steps_exercise
        exclude=('steps',)
#_________________________________________Training
class Comments_FileNumber_serialize(serializers.ModelSerializer):
    class Meta:
        model =Comments_FileNumber_Training
        fields = ('Comments','id',)

class Answer_Exercise_serialize(serializers.ModelSerializer):
    class Meta:
        model =Answer_Exercise
        fields = ('Answer','id')

class List_Answer_Exercise_serialize(serializers.ModelSerializer):
    class Meta:
        model =Answer_Exercise
        fields = ('Answer','Exercise','id')
# ________________________________Behavior

class Chidren_behavior_list_serialize(serializers.ModelSerializer):
    class Meta:
        model=Children_behavior
        fields = ('Behavior_name','id',)

class Chidren_behavior_Update_Retrive_Create_serialize(serializers.ModelSerializer):
    class Meta:
        model=Children_behavior
        fields = ('Behavior_name','id',)
#__________________________________________Description of behaviors
class Descript_behavior_serialize(serializers.ModelSerializer):
    class Meta:
        model = Descript_behavior
        exclude=('Behavior','user')

class record_behavior_Weekly_serialize(serializers.ModelSerializer):
    class Meta:
        model = record_behavior_Weekly
        exclude=('behavior','user')
#______________________Step _2
class Cause_list_serialize(serializers.ModelSerializer):
    class Meta:
        model = Cause_list
        fields = '__all__'


class Cause_file_number_serialize(serializers.ModelSerializer):
    class Meta:
        model = Cause_file_number
        fields = ('Cause','id')


#_______________________Step_3 and 4

class Type_Rewards_serialize(serializers.ModelSerializer):
    class Meta:
        model = type_of_Rewrard
        fields = '__all__'



class Rewards_serialize(serializers.ModelSerializer):
    class Meta:
        model = Rewards
        fields = '__all__'


class Reward_behavior_serialize(serializers.ModelSerializer):
    class Meta:
        model = Rewards_behavior
        exclude =('user','behavior')

class Rules_Reward_serialize(serializers.ModelSerializer):
    class Meta:
        model =Rules_Reward
        exclude =('user','behavior' , )


class Create_Table_star_serialize(serializers.ModelSerializer):
    class Meta:
        model =Star_Table
        exclude =('user','Date_Time','behavior',)


class List_Table_star_serialize(serializers.ModelSerializer):
    class Meta:
        model =Star_Table
        exclude = ('behavior','Date_Time',)


class Create_Table_surprise_serialize(serializers.ModelSerializer):
    class Meta:
        model =Surprice_Table
        exclude =('user','Date_Time','behavior')

class List_Table_surprise_serialize(serializers.ModelSerializer):
    class Meta:
        model =Surprice_Table
        fields='__all__'

#_______________________________ Step 5 : punishment

class List_Punishment_recommend_serialize(serializers.ModelSerializer):
    class Meta:
        model =punishment_recommend
        fields='__all__'


class Create_Punishment_behavior_serialize(serializers.ModelSerializer):
    class Meta:
        model =Punishment_behavior
        exclude=('user','behavior','Date_Time')


class Punishment_behavior_serialize(serializers.ModelSerializer):
    class Meta:
        model =Punishment_behavior
        exclude=('user','behavior',)

#_____________________________Step 6 : situation_difficult

class Situation_defficult_behavior_serialize(serializers.ModelSerializer):
    class Meta:
        model =Situation_defficult_behavior
        exclude = ('user', 'behavior',)


#________________________________

class Create_Request_psy_serialize(serializers.ModelSerializer):
    first_name_psy = serializers.ReadOnlyField(source='user_psy.first_name')
    last_name_psy = serializers.ReadOnlyField(source='user_psy.last_name')
    class Meta:
        model =request_consultant
        exclude = ('user_request','file_number','date_request')



class List_Request_psy_serialize(serializers.ModelSerializer):
    first_name_psy = serializers.ReadOnlyField(source='user_psy.first_name')
    last_name_psy = serializers.ReadOnlyField(source='user_psy.last_name')
    class Meta:
        model =request_consultant
        fields = '__all__'


#________________________ Agenda of filenumber
class Create_Agenda_serialize(serializers.ModelSerializer):
    class Meta:
        model = Agenda_fileNumber
        fields = ('name','descript',)


class List_Agenda_serialize(serializers.ModelSerializer):
    class Meta:
        model = Agenda_fileNumber
        fields = '__all__'

class Retrieve_Agenda_serialize(serializers.ModelSerializer):
    class Meta:
        model = Agenda_fileNumber
        fields = ('name', 'descript','file_number','date_Agenda',)

#________________________ PSychology l

class List_new_request_serialize(serializers.ModelSerializer):
    class Meta:
        model =request_consultant
        exclude=('user_psy','date_active','user_request')



class View_file_number_consultant_serialize(serializers.ModelSerializer):
    class Meta:
        model =Children
        exclude = ('Parent',)
#_____________________________Ongoing consultions



class List_behavior_consultant_serialize(serializers.ModelSerializer):
    class Meta:
        model =Children_behavior
        fields = ('Behavior_name',)

class change_StausRequest_consultant_serialize(serializers.ModelSerializer):
    class Meta:
        model = request_consultant
        exclude = ('user_psy', 'date_active', 'user_request' , 'file_number' , 'date_request')

class Set_time_cost_filenumber_serialize(serializers.ModelSerializer):
    class Meta:
        model = Set_Time_Cost_filenumber
        exclude=('request',)
#____________________________Question_Answer of request
class Create_question_psy_serialize(serializers.ModelSerializer):
    class Meta:
        model = Answer_question_request
        exclude=('request','answer')

class Update_answer_parent_serialize(serializers.ModelSerializer):
    class Meta:
        model = Answer_question_request
        exclude=('request','question')

#_________________________Ongoing consultions

class List_ongoing_consultant_serialize(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user_request.username')
    class Meta:
        model =request_consultant
        exclude=('user_psy','user_request')


class noting_fileNumber_serialize(serializers.ModelSerializer):
    class Meta:
        model = notting_fileNumber
        exclude=('consultant','file_number')

class general_noting_serialize(serializers.ModelSerializer):
    class Meta:
        model =general_noting
        exclude=('consultant',)


class create_Helper_file_number_serialize(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='Helper.email')
    class Meta:
        model = Helper_file_number
        fields=('email','id')

class List_Helper_file_number_serialize(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='Helper.email')
    name=serializers.ReadOnlyField(source='Helper.first_name')
    family=serializers.ReadOnlyField(source='Helper.last_name')
    class Meta:
        model = Helper_file_number
        fields=('id','name','family','email')