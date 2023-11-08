from django import forms
from .models import PREFECTURE_CHOICES, DEVIATION_VALUE_CHOICES,Thread
from django.db import models
from .models import School, Prefecture, City, Deviation_Value, Score, Post
from accounts.models import CustomUser



class SearchForm(forms.Form):
    prefecture = forms.ChoiceField(choices=PREFECTURE_CHOICES, label='エリア')
    min_deviation = forms.IntegerField(label='最小偏差値', required=False)
    max_deviation = forms.IntegerField(label='最大偏差値', required=False)
    deviation_value = forms.ChoiceField(choices=DEVIATION_VALUE_CHOICES,label='偏差値')
    
    
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title','content', 'score' ]
        
    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        score_choices = Score.objects.all().order_by('value')
        self.fields['score'].choices = [(score.id, '★' * score.value) for score in score_choices]
    
    def __str__(self):
        return self.TimestampedModel
    

class PostForm(forms.ModelForm):
    school_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    city_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    school = forms.ModelChoiceField(queryset=School.objects.all(), required=False, empty_label=None)
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, empty_label=None)
    deviation_value = forms.ModelChoiceField(queryset=Deviation_Value.objects.all(), required=False, empty_label=None)
    prefecture = forms.ModelChoiceField(queryset=Prefecture.objects.all(), required=False, empty_label=None)



    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        school_id = kwargs.pop('school_id', None)
        city_id = kwargs.pop('city_id', None)

        super(PostForm, self).__init__(*args, **kwargs)
        score_choices = [(score.id, '★' * score.value) for score in Score.objects.all().order_by('value')]
        self.fields['score'].choices = score_choices
        
        if school_id is not None:
            self.fields['school_id'].initial = school_id
        if city_id is not None:
            self.fields['city_id'].initial = city_id
            try:
                self.fields['city'].initial = City.objects.get(pk=city_id)
            except City.DoesNotExist:
                pass

    class Meta:
        model = Post
        fields = ['school_id', 'city_id', 'school', 'title', 'content', 'score', 'deviation_value', 'prefecture', 'city']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        score = cleaned_data.get('score')

        if not title and not self._errors.get('title'):
            self.add_error('title', 'このフィールドは必須です.')
        if not content and not self._errors.get('content'):
            self.add_error('content', 'このフィールドは必須です.')
        if score is None and not self._errors.get('score'):
            self.add_error('score', 'このフィールドは必須です.')




def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # フォームデータを取得
        title = request.POST['title']
        content = request.POST['content']
        score = request.POST['score']
        prefecture = request.POST['prefecture']
        deviation_value = request.POST['deviation_value']
        city_id = request.POST['city']

        # フォームデータを更新
        post.title = title
        post.content = content
        post.score = score
        post.prefecture = prefecture
        post.deviation_value = deviation_value
        post.city_id = city_id

        post.save()

        messages.success(request, '投稿が更新されました。')
        return redirect('boards:post_detail', post_id=post.id)

    return render(request, 'boards/edit_post.html', {'post': post})