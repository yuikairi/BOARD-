from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm,UserEditForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        
        user = form.save()
        self.object = user
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    template_name = "signup_success.html"
    
@login_required
def edit_profile(request):
    context = {} 
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        messages.success(request, 'ユーザー情報が更新されました。')
        return render(request, 'profile.html', context)
    else:
        form = UserEditForm(instance=request.user)
    context['form'] = form
    storage = messages.get_messages(request)
    storage.used = True
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()

        messages.success(request, 'ユーザー情報が削除されました。')
     
        return redirect('profile')
    
    return render(request, 'delete_profile.html')
        
    
@login_required
def profile(request):
    try:
        user_profile = CustomUser.objects.get(username=request.user.username)
    except CustomUser.DoesNotExist:
        user_profile = None  
        messages.success(request, 'ユーザー情報が更新されました。')
    context = {
        'user_profile': user_profile,
    }
    print(user_profile)

    return render(request, 'profile.html', context)

