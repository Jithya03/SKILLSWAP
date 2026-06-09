from django.contrib import admin
from .models import Category,Skill,TeacherProfile,Rating,Message,LearnerProfile
# Register your models here.
admin.site.register(Category),
admin.site.register(Skill),
admin.site.register(TeacherProfile),
admin.site.register(Rating),
admin.site.register(Message),
admin.site.register(LearnerProfile),

from django.contrib import admin
from.models import EmailOTP
# Register your models here.

admin.site.register(EmailOTP)