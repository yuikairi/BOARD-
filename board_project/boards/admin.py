from django.contrib import admin
from .models import Post
from .models import (TimestampedModel, Deviation_Value, Prefecture, School, City, Score, Post, Thread)
    
class Deviation_ValueAdmin(admin.ModelAdmin):
    list_display = ['value']
   
class PrefectureAdmin(admin.ModelAdmin):
    list_display = ['prefecture_name']
   
    
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['school_name']
   

class CityAdmin(admin.ModelAdmin):
    list_display = ['city_name']
   

class ScoreAdmin(admin.ModelAdmin):
    list_display = ['value']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title']

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['content']
    
    
admin.site.register(Post,PostAdmin)
admin.site.register(Deviation_Value,Deviation_ValueAdmin)
admin.site.register(Prefecture,PrefectureAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(City,CityAdmin)    
admin.site.register(Score,ScoreAdmin)
admin.site.register(Thread,ThreadAdmin)    