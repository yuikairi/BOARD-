from django.db import models
from datetime import datetime
from accounts.models import CustomUser
from django.db.models import Q
import logging
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from .rating import Rating 

class TimestampedModel(models.Model):
    #抽象ベースクラス。すべてのモデルで共通の created_at と updated_at フィールドを持たせる。
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # これが抽象ベースクラスであることを示す。このクラス自体はDBテーブルを持たない。      
      
class SchoolSearchQuerySet(models.QuerySet):
    def filter_by_prefecture(self, prefecture):
        return self.filter(prefecture__prefecture_name=prefecture)

    def filter_by_deviation_value(self, deviation_value):
        return self.filter(deviation_values=deviation_value)

def search_school(request):
    prefecture = request.GET.get('prefecture')
    deviation_value = request.GET.get('deviation_value')
    print(f'prefecture: {prefecture}')
    print(f'deviation_value: {deviation_value}')
    
    # カスタムクエリセット
    schools = School.objects.all()

    if prefecture:
        schools = schools.filter_by_prefecture(prefecture)
    if deviation_value:
        schools = schools.filter_by_deviation_value(deviation_value)


    if prefecture == "愛知" and deviation_value == "1":
        schools = schools.filter(deviation_values__in=[1, 2, 3, 4])  
    elif prefecture == "岐阜" and deviation_value == "2":
        schools = schools.filter(deviation_values__in=[1, 2, 3, 4])
    elif prefecture == "三重" and deviation_value == "3":
        schools = schools.filter(deviation_values__in=[1, 2, 3,4])                                                  
    return render(request, 'boards/school_list.html', {'schools': schools})

DEVIATION_VALUE_CHOICES = [
        ('1', '35~45'),
        ('2', '46~55'),
        ('3', '56~65'),
        ('4', '66以上'),
    ]
class Deviation_Value(TimestampedModel):
    users = models.ManyToManyField(CustomUser, blank=True)
    value = models.CharField(max_length=50, choices=DEVIATION_VALUE_CHOICES)
    school = models.ManyToManyField('School', related_name='deviation_value_schools_set')
    prefecture = models.ManyToManyField('Prefecture', related_name='deviation_values_set')
    city = models.ManyToManyField('boards.City', blank=True, related_name='deviation_values_set')
    
    def __str__(self):
        return self.get_value_display()  # 選択肢の表示名を取得

    
PREFECTURE_CHOICES = [
        ('愛知', '愛知'),
        ('岐阜', '岐阜'),
        ('三重', '三重'),
    ]
class Prefecture(TimestampedModel):
  users = models.ManyToManyField(CustomUser,blank=True)
  prefecture_name = models.CharField(max_length=255, choices=PREFECTURE_CHOICES,unique=True,null=True)
  deviation_value = models.ManyToManyField(Deviation_Value, blank=True, related_name='related_prefectures')
  school = models.ForeignKey('boards.School', on_delete=models.CASCADE, related_name='related_prefecture_schools', null=True)

  
  def __str__(self):
        return self.prefecture_name

class School(TimestampedModel):
    users = models.ManyToManyField(CustomUser,blank=True)
    school_name = models.CharField(max_length=50, unique=True,null=True)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, related_name='schools',null=True, blank=True)
    deviation_values = models.ManyToManyField(Deviation_Value, blank=True, related_name='schools')
    score = models.ManyToManyField('boards.Score',blank=True)
    city = models.ManyToManyField('boards.City',blank=True)
    
    objects = SchoolSearchQuerySet.as_manager() 
    
    def __str__(self):
        return self.school_name
        

class City(TimestampedModel):
  city_name = models.CharField(max_length=100, unique=True)
  prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, null=True)
  users = models.ManyToManyField(CustomUser,blank=True)
  deviation_value = models.ManyToManyField(Deviation_Value, blank=True, related_name='related_citys')
  
  def __str__(self):
        return self.city_name
      
      
SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

class Score(TimestampedModel):
   value = models.IntegerField('boards.Scores', blank=True, 
    choices=SCORE_CHOICES, default='3',unique=True)
   city = models.ManyToManyField(City,blank=True)
   users = models.OneToOneField(CustomUser, on_delete=models.PROTECT,unique=True,null=True)
   
   
   class Meta:
        unique_together = ('value', 'users')

   def get_percent(self):
        percent = round(self.score / 5 * 100)  
        return percent


class Post(TimestampedModel):
    title = models.CharField(verbose_name='タイトル', max_length=100)
    content = models.TextField(verbose_name='本文')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='related_posts', null=True, blank=True)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    deviation_value = models.ForeignKey(Deviation_Value, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    total_rating = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=get_user_model)
    
    def calculate_score(self):
        ratings = Rating.objects.filter(post=self)
        total_rating = sum(rating.value for rating in ratings)
        
        self.total_rating = total_rating
        self.save()
    
    def __str__(self):
        return f'{self.title} - 学校名: {self.school.school_name}, - 都道府県: {self.prefecture.prefecture_name}, 市: {self.city.city_name} ,レビュー: {self.score.value} ,偏差値: {self.deviation_value.get_value_display()}'

     
    
class Thread(TimestampedModel):
    users = models.ManyToManyField(CustomUser,blank=True)
    content = models.TextField(verbose_name='本文')
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    deviation_value = models.ForeignKey('boards.Deviation_Value', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    def __str__(self):
        return self.title
      
class SchoolSearchQuerySet(models.QuerySet):
    def filter_by_prefecture(self, prefecture):
        return self.filter(prefecture__prefecture_name=prefecture)

    def filter_by_deviation_value(self, deviation_value):
        return self.filter(deviation_values=deviation_value)

def search_school(request):
    prefecture = request.GET.get('prefecture')
    deviation_value = request.GET.get('deviation_value')
    print(f'prefecture: {prefecture}')
    print(f'deviation_value: {deviation_value}')
    
    # カスタムクエリセット
    schools = School.objects.all()

    if prefecture:
        schools = schools.filter_by_prefecture(prefecture)
    if deviation_value:
        schools = schools.filter_by_deviation_value(deviation_value)


    if prefecture == "愛知" and deviation_value == "1":
        schools = schools.filter(deviation_values__in=[1, 2, 3, 4])  # 35〜45に対応する値を指定
    elif prefecture == "岐阜" and deviation_value == "2":
        schools = schools.filter(deviation_values__in=[1, 2, 3, 4])
    elif prefecture == "三重" and deviation_value == "3":
        schools = schools.filter(deviation_values__in=[1, 2, 3,4])                                                  
    return render(request, 'boards/school_list.html', {'schools': schools})

