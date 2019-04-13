# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User,Permission



# Create your models here.
# class for eduction speciality which psychology have
class Speciality_Education_psy(models.Model):
    id = models.AutoField(primary_key=True)
    txt_en = models.CharField(max_length=100)
    txt_fr = models.CharField(max_length=250)
# list of jobs
class Jobs_Parents(models.Model):
    id = models.AutoField(primary_key=True)
    txt_en = models.CharField(max_length=250)
    txt_fr = models.CharField(max_length=250)

# for complete profile of parents
class Profile_Parents(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE , related_name='parents' , db_column='user')
    Birth_date=models.DateField()
    matrial_status=models.CharField(max_length=250)
    jobs=models.CharField(max_length=250)
    education_degree=models.IntegerField()

# for complete profile of psycology
class Profile_Psy(models.Model): # Psy is abbreviation of psychology
    user= models.ForeignKey(User, on_delete=models.CASCADE ,related_name='psychology', db_column='user')
    education_degree=models.IntegerField() # code of educations
    profile_image_psy=models.ImageField(upload_to='pic_profile_psy_folder/')
    Specialist_in_Field_work=models.TextField()
    biography=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2) #
    during_session=models.DurationField() # is accoriding to minutes
    Code_organization=models.IntegerField()
# prifile of childern of parents
class Children(models.Model):
    Parent=models.ForeignKey(User, on_delete=models.CASCADE , db_column='parent')
    file_number=models.AutoField(primary_key=True)
    name=models.CharField(max_length=250 , null=False)
    family = models.CharField(max_length=250, null=False)
    date_birthday=models.DateField()
    grade_Educations=models.IntegerField()
    disability= models.BooleanField(default=False,)
    mental_problems= models.TextField(null=True, blank=True)
    Physical_problems = models.TextField(null=True, blank=True)
    Date_create=models.DateField()

#_______________________________________________
# Manage Training Steps
class Steps_training(models.Model):
    id=models.AutoField(primary_key=True)
    name_Steps=models.CharField(max_length=255 , null=False , verbose_name="نام مرحله آمورشی ")
    text_Training_steps=models.TextField(null=False ,verbose_name="متن آموزشی",)
    example_Training_steps = models.TextField(null=True ,verbose_name="مثال های مرحله آموزشی")
    question_common_Training_steps = models.TextField(null=True, verbose_name="پرسش های متداول مرحله آموزشی ")

    def __str__(self):
        return format(self.name_Steps)

    class Meta:
        verbose_name = 'مدیریت مرحله آموزشی '
        verbose_name_plural = 'مدیریت مراحل آمورشی'
#_____________________________________________________________________________
# Manage Exercise of Training Steps
class Steps_exercise(models.Model):
    id = models.AutoField(primary_key=True)
    steps=models.ForeignKey(Steps_training,on_delete=models.CASCADE,db_column='steps' ,verbose_name="مربوط به کدام مرحله آموزش ")
    exercise_name = models.CharField(max_length=255,verbose_name="نام مرحله تمرین ")
    exercise_text=models.TextField(verbose_name="متن مرحله آمورشی ")
    def __str__(self):
        return format(self.exercise_name)

    class Meta:
        verbose_name = 'مدیریت  تمرین آموزش '
        verbose_name_plural = 'مدیریت تمرینات آمورشی'


# Manage Comments Relations of File_numer to Comments of Steps Training
class Comments_FileNumber_Training(models.Model):
    id = models.AutoField(primary_key=True)
    file_number=models.ForeignKey(Children,on_delete=models.CASCADE,db_column='file_number')
    Steps = models.ForeignKey(Steps_training, on_delete=models.CASCADE, db_column='Steps')
    Comments=models.TextField()

# Manage Answer of Exercise:
class Answer_Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    file_number=models.ForeignKey(Children,on_delete=models.CASCADE,db_column='file_number')
    Exercise = models.ForeignKey(Steps_exercise, on_delete=models.CASCADE, db_column='Steps_Exercise')
    Answer=models.TextField()
#______________________________Manage of Steps 1

class Children_behavior(models.Model):
    id=models.AutoField(primary_key=True)
    file_number = models.ForeignKey(Children, on_delete=models.CASCADE, db_column='file_number')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User')
    Behavior_name=models.CharField(max_length=255)

class Descript_behavior(models.Model):
    id = models.AutoField(primary_key=True)
    Behavior=models.ForeignKey(Children_behavior,on_delete=models.CASCADE,db_column='behavior')
    discrip=models.TextField(null=True)
    date_time= models.DateTimeField()
    place=models.CharField(max_length=255)
    Status_before_bahavior=models.TextField()
    Result_behavior=models.TextField()
    Comments=models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User')


class record_behavior_Weekly(models.Model):
    id = models.AutoField(primary_key=True)
    behavior=models.ForeignKey(Children_behavior,on_delete=models.CASCADE,db_column='behavior')
    date=models.DateTimeField()
    Times=models.IntegerField() # this times of behavior
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User')
#____________________________________________Stpe_2

class Cause_list(models.Model):
    id = models.AutoField(primary_key=True)
    Cause_txt=models.CharField(max_length=255 , verbose_name='نام دلیل ')
    Cause_descript=models.TextField(verbose_name='شرح مختصری ار دلایل مورد نظر')
    def __str__(self):
        return format(self.Cause_txt)

    class Meta:
        verbose_name = 'مدیریت  دلیل رفتاری '
        verbose_name_plural = 'مدیریت دلایل رفتاری'

class Cause_file_number(models.Model):
    id = models.AutoField(primary_key=True)
    behavior=models.ForeignKey(Children_behavior,on_delete=models.CASCADE,db_column='behavior')
    Cause= models.ForeignKey(Cause_list,on_delete=models.CASCADE,db_column='Cause')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User')
#_____________________________________Step 3 and 4

class type_of_Rewrard(models.Model):
    id = models.AutoField(primary_key=True)
    txt = models.CharField(max_length=255, verbose_name='نوع پاداش ')
    descript = models.TextField(verbose_name='شرح مختصری ار نوع پاداش مورد نظر', null=True , )
    def __str__(self):
        return format(self.txt)

    class Meta:
        verbose_name = 'مدیریت  نوع پاداش رفتاری '
        verbose_name_plural = 'مدیریت انواع پاداش  رفتاری '

class Rewards(models.Model):
    id = models.AutoField(primary_key=True)
    Reward_txt = models.CharField(max_length=255, verbose_name='نام پاداش ')
    Reward_descript = models.TextField(verbose_name='شرح مختصری ار پاداش مورد نظر')
    type_of_Reward=models.ForeignKey(type_of_Rewrard, on_delete=models.CASCADE, db_column='type_reward')

    def __str__(self):
        return format(self.Reward_txt)

    class Meta:
        verbose_name = 'مدیریت  پاداش رفتاری پیشنهاد شده به کاربر '
        verbose_name_plural = 'مدیریت پاداش های رفتاری پیشنهاد شده به کاربر '


class Rewards_behavior(models.Model):
    id = models.AutoField(primary_key=True)
    Reward_txt = models.CharField(max_length=255, verbose_name='نام پاداش ')
    Reward_descript = models.TextField(null=True,verbose_name= 'شرح مختصری ار پاداش مورد نظر')
    type_of_Reward=models.ForeignKey(type_of_Rewrard, on_delete=models.CASCADE, db_column='type_reward')
    behavior=models.ForeignKey(Children_behavior,on_delete=models.CASCADE,db_column='behavior')
    user=models.ForeignKey(User,on_delete=models.CASCADE,db_column='user')

class Rules_Reward(models.Model):
    id = models.AutoField(primary_key=True)
    Rule_txt = models.CharField(max_length=255,)
    Rule_descript = models.TextField()
    Reward = models.ForeignKey(Rewards_behavior, on_delete=models.CASCADE, db_column='Reward')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')

class Star_Table(models.Model):
    id = models.AutoField(primary_key=True)
    reward_rule=models.ForeignKey(Rules_Reward,on_delete=models.CASCADE , db_column='reward_rule')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    Date_Time=models.DateTimeField()


class Surprice_Table(models.Model):
    id = models.AutoField(primary_key=True)
    Reward=models.ForeignKey(Rewards_behavior,on_delete=models.CASCADE ,db_column='bahavior_reward')
    behavior=models.ForeignKey(Children_behavior,on_delete=models.CASCADE ,db_column='behavior')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    Date_Time=models.DateTimeField()


class punishment_recommend(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='نام تنبیه ')
    descript = models.TextField(verbose_name='شرح مختصری ار تنبیه مورد نظر')

    def __str__(self):
        return format(self.name)

    class Meta:
        verbose_name = 'مدیریت  تنبیه پیشنهاد شده به کاربر '
        verbose_name_plural = 'مدیریت تنبیه های  پیشنهاد شده به کاربر '



class Punishment_behavior(models.Model):
    id=models.AutoField(primary_key=True)
    behavior = models.ForeignKey(Children_behavior, on_delete=models.CASCADE, db_column='behavior')
    name=models.CharField(max_length=255)
    descript = models.TextField(null=True)
    result=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    Date_Time=models.DateTimeField()

class Situation_defficult_behavior(models.Model):
    id=models.AutoField(primary_key=True)
    behavior = models.ForeignKey(Children_behavior, on_delete=models.CASCADE, db_column='behavior')
    name=models.CharField(max_length=255)
    comments = models.TextField(null=True)
    grade=models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    Date_Time = models.DateTimeField()


class request_consultant(models.Model):

    Pending=1
    Reject=0
    Accept=2
    Activate = (
        (Pending, 'Pending'),
        (Accept, 'Accept'),
        (Reject,'Reject')
    )
    id = models.AutoField(primary_key=True)
    user_request = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_request' , related_name='user_request')
    user_psy = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_psy',related_name='user_psy')
    date_request=models.DateField()
    file_number=models.ForeignKey(Children, on_delete=models.CASCADE ,  db_column='file_number')
    activ_req=models.IntegerField(default=1, choices=Activate)
    date_active=models.DateField(null=True)

class Agenda_fileNumber(models.Model):
    id = models.AutoField(primary_key=True)
    user_psy = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_psy')
    file_number = models.ForeignKey(Children, on_delete=models.CASCADE, db_column='file_number')
    date_Agenda = models.DateField()
    name=models.CharField(max_length=255)
    descript=models.TextField()


#--------------------Psychology : New Request

class Set_Time_Cost_filenumber(models.Model):
    id = models.AutoField(primary_key=True)
    request=models.ForeignKey(request_consultant,on_delete=models.CASCADE,db_column='request')
    duration=models.DurationField()
    Cost=models.IntegerField()
    comment=models.TextField()

class Answer_question_request(models.Model):
    id = models.AutoField(primary_key=True)
    request = models.ForeignKey(request_consultant, on_delete=models.CASCADE, db_column='request')
    question = models.TextField()
    answer =models.TextField()
#_______________________Ongoing consultant

class notting_fileNumber(models.Model):
    id = models.AutoField(primary_key=True)
    consultant=models.ForeignKey(User,on_delete=models.CASCADE, db_column='consultant')
    file_number=models.ForeignKey(Children,on_delete=models.CASCADE, db_column='file_number')
    txt=models.TextField()

class general_noting(models.Model):
    id = models.AutoField(primary_key=True)
    consultant = models.ForeignKey(User, on_delete=models.CASCADE, db_column='consultant')
    txt = models.TextField()


class Helper_file_number(models.Model):
    id = models.AutoField(primary_key=True)
    Helper = models.ForeignKey(User, on_delete=models.CASCADE, db_column='helper')
    file_number = models.ForeignKey(Children, on_delete=models.CASCADE, db_column='file_number')