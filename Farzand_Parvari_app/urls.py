from django.conf.urls import include, url
from django.conf import settings
import django.contrib.auth.views as auth_views
from rest_framework import routers
import Farzand_Parvari_app.views as views
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView,
    PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
        )
from .View_API import (TestAuthView,
                       LogoutViewEx ,
                       Profile_Parents_view,
                       Profile_Psychology_view,
                    Retrive_Update_Profile_Parents,
                    Retrive_Update_Profile_Psy,
                    Children_Create,
                    Children_List,
                    Children_Update,
                    Steps_Training_List,
                    Steps_Exercise_List,
                    Create_Comments_steps,
                    Update_Retrive_Comments_steps,
                    Create_Answer_Exercise,
                    Update_Retrive_Answer_Exercise,
                    List_answer_exer,
                    Create_bahavior,
                    Update_Retrive_Behavior,
                    List_bahavior,
                    Create_descriptions,
                    List_descripttions,
                    Update_Retrive_descriptions,
                    Create_record_weekly,
                    List_Record_Bahavior,
                    Update_Retrive_record_weekly,
                    List_Cause_List,
                    Create_Cause_file_number,
                    List_Cause_file_number,
                    Update_Retrive_Cause_file_number,
                    List_Rewards,
                    List_type_Rewards,
                    Create_Rewards_behavior,
                    List_Reward_behavior,
                    Update_Retrive_Reward_behavior,
                    Create_Rule_Rewards,
                    List_Rule_Reward,
                    Update_Retrive_Rule_Reward,
                    Create_Star_Table,
                    List_Star_Table,
                    Update_Retrive_Table_Star,
                    Create_Surprise_Table,
                    List_surprise_table,
                    List_punishment_recommend,
                    Create_Punishment_behavior,
                    List_Punishment_behavior,
                    Update_Retrive_Punishment_behavior,
                    Create_Situation_behavior,
                    List_Situation_behavior,
                    Update_Retrive_Situation_behavior,
                    List_all_Psy,
                    Create_request_psy,
                    List_request_psy,
                    Update_Retrive_request_psy,
                    Create_Agenda_File_Number,
                    List_Agenda,
                    Update_Retrive_Agenda,
                    List_new_request,
                    View_file_number_psy,
                    View_behavior_psy,
                    Change_status_request,
                    List_Create_time_cost,
                    Retrieve_update_time_cost,
                    List_Create_question_request,
                    Update_Retrieve_Answer_request,
                    List_ongoing_request,
                    List_Create_noting_fileNumber,
                    Retrieve_update_noting_file_number,
                    List_Create_general_noting,
                    Retrieve_update_general_noting,
                    List_Create_Helper_file_number,
                    Retrieve_delete_Helper_file_number
                       )
urlpatterns = [
    url(r'check_member/$',views.check_member),
    url(r'^Register_Admin/$', views.Create_admin_site, name='register_Admin'),
    url(r'^Register_Parents/$', views.register_parents, name='register_Parents'),
    url(r'^Register_Psychology/$', views.register_psychology, name='register_Psychology'),
    url(r'^Register_Helper/$', views.register_helper, name='register_helper'),
    # Profile
    url(r'^Profile_Parents_Create/$', Profile_Parents_view.as_view()),
    url(r'^Profile_Psychology_Create/$', Profile_Psychology_view.as_view()),
    url(r'^Profile_Parents_Update/$', Retrive_Update_Profile_Parents.as_view()),
    url(r'^Profile_Psychology_Update/$', Retrive_Update_Profile_Psy.as_view()),

    # User authentications
    url('logout/', LogoutViewEx.as_view(), name='rest_logout', ),# that overrides the rest-auth REST logout-view (
    url('login/', LoginView.as_view(), name='rest_login', ), #  the rest-auth REST login-view
    url(r'^password/reset/$', PasswordResetView.as_view(),name='rest_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^password/change/$', PasswordChangeView.as_view(),name='rest_password_change'),
    # children
    url(r'^Children_Create/$', Children_Create.as_view(),name='Create_Chidren'),
    url(r'^Children_List/$', Children_List.as_view(),name='List_Chidren'),
    url(r'^Children_Retrive_Update/(?P<file_number>\d{8})/$', Children_Update.as_view(),name='Update_Retrive_Chidren'),
    # List all of the Steps of Training
    url(r'^Steps_Training_List/$', Steps_Training_List.as_view(),name='Steps_training_List'),
    #List all of the Excrecise
    url(r'^Steps_Exercise_List/(?P<training_id>\d+)/$', Steps_Exercise_List.as_view(),name='Steps_Exercise_List'),
    # Comments on Training Steps
    url(r'^Create_Comments_Steps/(?P<file_number>\d{8})/(?P<step_id>\d+)/$', Create_Comments_steps.as_view(),name='Create_Comments_Chidren'),
    url(r'^Update_Comments_Steps/(?P<file_number>\d{8})/(?P<step_id>\d+)/$',Update_Retrive_Comments_steps.as_view(),name='Update_Retrive_Comments'),
    # Answer to Exercise
    url(r'^Create_Answer_exer/(?P<file_number>\d{8})/(?P<exercise_id>\d+)/$', Create_Answer_Exercise.as_view(),name='Create_Comments_Answer'),
    url(r'^List_Answer_exer/(?P<file_number>\d{8})/$', List_answer_exer.as_view(),name='Liste_Eercise_Answer'),
    url(r'^Update_Answer_exer/(?P<file_number>\d{8})/(?P<exercise_id>\d+)/$',Update_Retrive_Answer_Exercise.as_view(),name='Update_Retrive_Answer'),
    # Behavior
    url(r'^Create_bahavior/(?P<file_number>\d{8})/$', Create_bahavior.as_view(),name='Create_behavior'),
    url(r'^List_bahavior/(?P<file_number>\d{8})/$', List_bahavior.as_view(),name='List_behavior'),
    url(r'^Update_Retrieve_bahavior/(?P<file_number>\d{8})/(?P<id_behavior>\d+)/$', Update_Retrive_Behavior.as_view(),name='Update_Retrive_Behavior'),
    # Descrip_Bahaviors
    url(r'^Create_descript/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', Create_descriptions.as_view(),name='Create_Description'),
    url(r'^List_descript/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', List_descripttions.as_view(),name='List_Description'),
    url(r'^Update_descript/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<descript_id>\d+)/$',Update_Retrive_descriptions.as_view(),name='Update_Retrieve_Description'),
    # Record behavior weekly
    url(r'^Create_record_weekly/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', Create_record_weekly.as_view(),name='Create_behaviors_weekly'),
    url(r'^List_record_weekly/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', List_Record_Bahavior.as_view(),name='List_Record_Bahavior'),
    url(r'^Update_record_weekly/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<record_weekly_id>\d+)/$',Update_Retrive_record_weekly.as_view(),name='Update_Retrieve_Record_weekly'),
    # Cause
    url(r'^list_cause/$',List_Cause_List.as_view(),name='List_Cause_List'),
    # Cause_file_number
    url(r'^Create_Cause_file_numbe/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', Create_Cause_file_number.as_view(),name='Create_Cause_file_number'),
    url(r'^List_Cause_file_numbe/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$',List_Cause_file_number.as_view(),name='List_Cause_file_numbe'),
    url(r'^Update_Cause_file_numbe/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<Cause_file_id>\d+)/$',Update_Retrive_Cause_file_number.as_view(),name='Update_Retrieve_Cause_file_number'),
    # Step 3 and 4
    url(r'^List_type_Rewards/$',List_type_Rewards.as_view(),name='List_type_Rewards'),
    url(r'^list_rewards/$',List_Rewards.as_view(),name='List_Rewards'),
    # Reward of Behavior
    url(r'^Create_Reward_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', Create_Rewards_behavior.as_view(),name='Create_Rewards_behavior'),
    url(r'^List_Reward_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$',List_Reward_behavior.as_view(),name='List_Reward_behavior'),
    url(r'^Update_Reward_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<Reward_id>\d+)/$',Update_Retrive_Reward_behavior.as_view(),name='Update_Retrieve_Reward_behavior'),
    # Rule of Rewards
    url(r'^Create_Rule_Rewards/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<reward_id>\d+)/$', Create_Rule_Rewards.as_view(),name='Create_Rule_Rewards'),
    url(r'^List_Rule_Reward/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<reward_id>\d+)/$', List_Rule_Reward.as_view(),name='List_Rule_Rewards'),
    url(r'^Update_Retrieve_Rule_Reward/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<reward_id>\d+)/(?P<rule_id>\d+)/$',Update_Retrive_Rule_Reward.as_view(),name='Update_Retrive_Rule_Reward'),
    #Star_table
    url(r'^Create_Star_Table/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<reward_id>\d+)/(?P<rule_id>\d+)/$', Create_Star_Table.as_view(),name='Creat_Star_Table'),
    url(r'^List_Star_Table/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<reward_id>\d+)/(?P<rule_id>\d+)/$',List_Star_Table.as_view(), name='List_Star_Table'),
    url(r'^Update_Retrieve_Star_Table/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<reward_id>\d+)/(?P<rule_id>\d+)/(?P<id>\d+)/$',Update_Retrive_Table_Star.as_view(),name='Update_Retrive_Rule_Reward'),
    # Surprise Table
    url(r'^Create_Surprise_Table/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', Create_Surprise_Table.as_view(),name='Create_Surprise_Table'),
    url(r'^List_Surprise_Table/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', List_surprise_table.as_view(),name='List_Star_Table'),
    #Punishment 5
    url(r'^list_punishment_recommend/$',List_punishment_recommend.as_view(),name='List_punishment_recommend'),
    url(r'^Create_punishment_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', Create_Punishment_behavior.as_view(),name='Create_Punishment_behavior'),
    url(r'^List_punishment_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$',List_Punishment_behavior.as_view(),name='List_punishment_behavior'),
    url(r'^Update_punishment_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<Punish_id>\d+)/$',Update_Retrive_Punishment_behavior.as_view(),name='Update_Retrive_Punishment_behavior'),
    # Difficult Situations
    url(r'^Create_Situation_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$', Create_Situation_behavior.as_view(),name='Create_Situation_behavior'),
    url(r'^List_Situation_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/$',List_Situation_behavior.as_view(),name='List_Situation_behavior'),
    url(r'^Update_Retrive_Situation_behavior/(?P<file_number>\d{8})/(?P<behavior_id>\d+)/(?P<situation_id>\d+)/$',Update_Retrive_Situation_behavior.as_view(),name='Update_Retrive_Situation_behavior'),
    # Request Consultant
    url(r'^List_Psychology/$',List_all_Psy.as_view(),name='List_all_psy'),
    url(r'^Create_Request_file_number/(?P<file_number>\d{8})/$', Create_request_psy.as_view(),name='Create_request_psy'),
    url(r'^List_Request_file_number/(?P<file_number>\d{8})/$', List_request_psy.as_view(),name='List_request_psy'),
    url(r'^Update_Retrieve_Request_psy/(?P<file_number>\d{8})/(?P<id_request>\d+)/$',Update_Retrive_request_psy.as_view(),name='Update_Retrive_request_psy'),
    # Agenda
    url(r'^Create_Agenda/(?P<file_number>\d{8})/$', Create_Agenda_File_Number.as_view(),name='Create_Agenda_File_Number'), # just Psychology
    url(r'^List_Agenda/(?P<file_number>\d{8})/$', List_Agenda.as_view(),name='List_Agenda'),
    url(r'^Update_Retrieve_Agenda/(?P<file_number>\d{8})/(?P<id_agenda>\d+)/$',Update_Retrive_Agenda.as_view(),name='Update_Retrive_Agenda'),
    #____________________________________________________Psychology

    #new request:
    url(r'^List_new_request/$', List_new_request.as_view(),name='List_new_request'),
    url(r'^View_FileNumber_Psy/(?P<file_number>\d{8})/$', View_file_number_psy.as_view(),name='View_file_number_psy'),
    url(r'^View_behavior_Psy/(?P<file_number>\d{8})/$', View_behavior_psy.as_view(),name='View_behavior_psy'),
    url(r'^Change_status_request/(?P<id_request>\d+)/$', Change_status_request.as_view(),name='Change_status_request'),
    # Set time cost for request
    #if user is parents can visit retrive of instance of models and user is psychology can create and retrieve
    url(r'^Create_time_cost_request/(?P<id_request>\d+)/$', List_Create_time_cost.as_view(),name='List_Create_time_cost'),
    #if user is parents can visit retrive of instance of models and user is psychology can update and retrieve
    url(r'^Update_Retrieve_time_cost_request/(?P<request_id>\d+)/$', Retrieve_update_time_cost.as_view(),name='Retrieve_update_time_cost'),
    # Question Answer on request
    # Create question by consultant but list question  by parent and psychology
    url(r'^Create_list_question_request/(?P<id_request>\d+)/$', List_Create_question_request.as_view(),name='List_Create_question_request'),
    # when update answer to question by parents or pychology
    url(r'^Update_Retrieve_Answer/(?P<id_request>\d+)/(?P<id>\d+)/$', Update_Retrieve_Answer_request.as_view(),name='Retrieve_update_time_cost'),
    url(r'^List_ongoing_request/$', List_ongoing_request.as_view(),name='List_ongoing_request'),
    # Noting_fileNumber
    url(r'^List_create_noting_fileNumber/(?P<file_number>\d{8})/$', List_Create_noting_fileNumber.as_view(),name='List_Create_noting_fileNumber'),
    url(r'^Retrieve_update_noting_fileNumber/(?P<file_number>\d{8})/(?P<id>\d+)/$', Retrieve_update_noting_file_number.as_view(),name='Retrieve_update_noting_file_number'),
    # general  Noting
    url(r'^List_create_general_nothing/$', List_Create_general_noting.as_view(),name='List_Create_general_noting'),
    url(r'^Retrieve_update_general_noting/(?P<id>\d+)/$', Retrieve_update_general_noting.as_view(),name='Retrieve_update_general_noting'),
    # Helper_File_number
    url(r'^List_create_helper_fileNumber/(?P<file_number>\d{8})/$', List_Create_Helper_file_number.as_view(),name='List_Create_Helper_file_number'),
    url(r'^Retrieve_delete_helper_fileNumber/(?P<file_number>\d{8})/(?P<id>\d+)/$', Retrieve_delete_Helper_file_number.as_view(),name='Retrieve_update_Helper_file_number'),
    #add role helper to request user
    url(r'^active_role_helper/$', views.active_role_helper,name='active_role_helper'),

]