from django.shortcuts import render, redirect,get_object_or_404
from .models import Post, Thread, School,City,Deviation_Value
from .forms import SearchForm, ThreadForm, SearchForm,PostForm
from django.views.generic import  TemplateView, CreateView,DeleteView
from functools import reduce
from operator import and_ 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from accounts.models import CustomUser
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseNotFound,HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.db import models
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
import logging
from django.views.generic.list import ListView


def post_list(request,post_id=None):
    posts = Post.objects.all().order_by('-created_at') 
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    custom_user = request.user
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'boards/post_list.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    posts = Post.objects.all()
    post = get_object_or_404(Post, id=post_id)
    custom_user = request.user 
    threads = Thread.objects.filter(post=post)
    new_thread = None  
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            new_thread = form.save(commit=False)
            new_thread.post = post
            new_thread.user = request.user
            new_thread.save()
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            score = form.cleaned_data['score']
    form = ThreadForm()
    return render(request, 'boards/post_detail.html', {'post': post, 'threads': threads, 'form': form, 'thread_id': new_thread.id if new_thread else None})


def search_school(request):
    deviation_value = request.GET.get('deviation_value')
    deviation = Deviation_Value.objects.filter(value=deviation_value).first()
    prefecture_id = request.GET.get('prefecture_id')
    if request.method == 'POST'or request.method == 'GET':
        form = SearchForm(request.POST)
        if form.is_valid():
            schools = School.objects.filter(prefecture__prefecture_name=prefecture, deviation_values=deviation_value)
            schools = filter_school_queryset(schools)         
            return render(request, 'boards/school_list.html', {'schools': schools, 'form': form})
    else:
        form = SearchForm()  
    return render(request, 'boards/search_school.html', {'form': form})

def school_list(request):
    schools = School.objects.all()
    prefecture = request.GET.get('prefecture')
    deviation_value = request.GET.get('deviation_value')  
    print(f"deviation_value: {deviation_value}")
    min_deviation = request.GET.get('min_deviation')
    max_deviation = request.GET.get('max_deviation')
    if deviation_value is not None:
        try:
         deviation_value = int(deviation_value)
         schools = schools.filter(deviation_values__value=deviation_value)
        except ValueError as e:
            print(f"ValueError: {e}")
    else:
        deviation_value = 0    
    min_value = None  
    max_value = None  
    try:
        min_value = int(min_deviation) if min_deviation and min_deviation.isdigit() else None
    except ValueError:
        min_value = None
    try:
        max_value = int(max_deviation) if max_deviation and max_deviation.isdigit() else None
    except ValueError:
        max_value = None

    if prefecture:
        schools = schools.filter(prefecture__prefecture_name=prefecture)
    
    if min_value is not None:
        schools = schools.filter(deviation_values__value__gte=min_value)
    if max_value is not None:
        schools = schools.filter(deviation_values__value__lte=max_value)
        print(schools.query)
    if deviation_value:
        if deviation_value == '35-45':
            schools = schools.filter(deviation_values__value__range=(35, 45))
        elif deviation_value == '46-55':
            schools = schools.filter(deviation_values__value__range=(46, 55))
        elif deviation_value == '56-65':
            schools = schools.filter(deviation_values__value__range=(56, 65))
        elif deviation_value == '66以上':
            schools = schools.filter(deviation_values__value__gte=66)
                
    form = SearchForm(request.GET)
    
    if form.is_valid():
        prefecture = form.cleaned_data['prefecture']
        min_deviation = form.cleaned_data['min_deviation']
        max_deviation = form.cleaned_data['max_deviation']
        filtered_schools = School.objects.filter(prefecture__prefecture_name=prefecture)
        
        if min_deviation is not None:
            filtered_schools = filtered_schools.filter(deviation__gte=min_deviation)
        if max_deviation is not None:
            filtered_schools = filtered_schools.filter(deviation__lte=max_deviation)
        context = {'schools': filtered_schools, 'form': form, 'schools': schools,}
        return render(request, 'boards/school_list.html', context)
    else:
        form = SearchForm()
        print(form.errors)
    context = {'schools': schools, 'form': form,}
    return render(request, 'boards/school_list.html', context)


class IndexView(ListView):
    model = Post
    template_name = 'boards/index.html'
    context_object_name = 'orderby_records'
    queryset = Post.objects.order_by('-total_rating')
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ランキングデータを取得してcontextに追加
        top_ranked_posts = Post.objects.all().order_by('-total_rating')[:10]
        context['top_ranked_posts'] = top_ranked_posts
        return context

    
    

logger = logging.getLogger(__name__)
@method_decorator(login_required, name='dispatch')
class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "boards/post_create.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school_id'] = self.kwargs['school_id']
        kwargs['city_id'] = self.kwargs['city_id']
        logger.debug(f'self.kwargs["school_id"]: {self.kwargs["school_id"]}')
        logger.debug(f'self.kwargs["city_id"]: {self.kwargs["city_id"]}')

        return kwargs
    
    def get_success_url(self):
        school_id = self.kwargs.get('school_id')
        city_id = self.kwargs.get('city_id')
        return reverse_lazy('boards:post_done', args=[school_id, city_id])

    def form_valid(self, form):
        # フォームからデータを取得
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        score = form.cleaned_data['score']
        prefecture = form.cleaned_data['prefecture']
        deviation_value = form.cleaned_data['deviation_value']
        city = form.cleaned_data['city']
        
        logger.debug(f'City: {city}')
        logger.debug('Form is valid.')
        logger.debug(f'Title: {title}')
        logger.debug(f'Content: {content}')
        logger.debug(f'Score: {score}')
        logger.debug(f'Prefecture: {prefecture}')
        logger.debug(f'Deviation Value: {deviation_value}')
        logger.debug(f'City ID: {form.instance.city_id}')
        print =(city)
        # 学校オブジェクトを取得
        try:
            school = School.objects.get(id=self.kwargs['school_id'])
        except School.DoesNotExist:
            pass

        # city_idを取得（ログインユーザーに関連する情報）
        
        city_id = city.id if city else None
        logger.debug(f'City ID: {city_id}')
        
    # ユーザーIDを取得
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        if not city:
            # 学校に関連するCityを取得
            school_cities = school.city_set.all()
            if school_cities.exists():
                # 学校に関連するCityが存在する場合、最初のCityを選択
                default_city = school_cities.first()
            else:
                default_city = None
        else:
            # Cityが選択されている場合、そのCityを使用
            default_city = city

        # Cityをフォームに設定
        form.instance.city = default_city
        # 学校オブジェクトとcity_id、ユーザーIDをフォームに追加
        form.instance.school = school
        form.instance.city_id = city_id
        form.instance.user_id = user_id

        form.save()
        logger.debug(f'Post ID: {form.instance.id}')
        logger.debug(f'School ID: {form.instance.school_id}')
        logger.debug(f'City ID: {form.instance.city_id}')
        
        return redirect(self.get_success_url())

    
class PostSuccessView(TemplateView):
    template_name ='boards/post_success.html'

def school_detail(request, school_id):
    try:
        school = get_object_or_404(School, pk=school_id)
        cities = school.city.all()
        city_info_list = [{"id": city.id, "name": city.city_name} for city in cities]
        
        # 最初の都市を取得し、存在する場合に初期値を設定
        city = cities.first()
        initial = {}
        if city:
            initial['city'] = city

        form = PostForm(initial=initial)
        
    except School.DoesNotExist:
        error_message = "School does not exist"
        return HttpResponse(error_message, status=404)

    posts = Post.objects.filter(school=school)
    threads = Thread.objects.filter(post__in=posts)
    context = {
        'school': school,
        'school_id': school_id,
        'posts': posts,
        'threads': threads,
        'form': form,
        'city': city,  
    }
    return render(request, 'boards/school_detail.html', context)






    
def ranking_view(request):
        top_ranked_posts = Post.objects.all().order_by('-total_rating')[:10]
        return render(request, 'boards/ranking.html', {'top_ranked_posts': top_ranked_posts})

    
class PostSuccessView(TemplateView):
    template_name ='boards/post_success.html'

class DeleteSuccessView(TemplateView):
    template_name = 'boards/delete_success.html'
    
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('boards:delete_success')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user == request.user:
            # 削除処理を実行
            return super().delete(request, *args, **kwargs)
        else:
            # ユーザーが投稿の作者でない場合、別のURLにリダイレクト
            return redirect('boards:post_list')
        
        
#投稿編集
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('boards:post_detail', post_id=post.id) 
    else:
        form = PostForm(instance=post)
    
    return render(request, 'boards/edit_post.html', {'form': form, 'post': post})