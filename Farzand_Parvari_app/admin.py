# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Steps_exercise, Steps_training , Cause_list , Rewards, type_of_Rewrard , punishment_recommend

# Register your models here.
admin.site.register(Steps_training)

admin.site.register(Steps_exercise)
admin.site.register(Cause_list)
admin.site.register(type_of_Rewrard)
admin.site.register(Rewards)
admin.site.register(punishment_recommend)