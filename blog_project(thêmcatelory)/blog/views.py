from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Task, UserProfile, Category
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'color']
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'color']
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('categories')

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'blog/category_confirm_delete.html'
    success_url = reverse_lazy('categories')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        search_input = self.request.GET.get('search-area') or ''
        category_id = self.request.GET.get('category') or ''
        
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.get_queryset().filter(complete=False).count()
        context['user_profile'] = UserProfile.objects.get_or_create(user=self.request.user)[0]
        context['categories'] = Category.objects.filter(user=self.request.user)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['search_input'] = search_input
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'category', 'complete', 'image', 'link']
    success_url = reverse_lazy('task')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.complete:
            form.instance.completed_at = timezone.now()
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'category', 'complete', 'image', 'link']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        if form.instance.complete and not form.instance.completed_at:
            form.instance.completed_at = timezone.now()
        elif not form.instance.complete:
            form.instance.completed_at = None
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('task') + '?updated=true'

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'blog/task.html'

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def form_valid(self, form):
        user = form.get_user()
        try:
            profile = UserProfile.objects.get(user=user)
            if profile.is_blocked:
                messages.error(self.request, "Tài khoản của bạn đã bị khóa!")
                return self.form_invalid(form)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=user, is_blocked=False)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task')

class RegisterPage(FormView):
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            UserProfile.objects.create(user=user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, *kwargs)

@login_required
def profile_view(request):
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'blog/profile.html', {
        'form': form,
        'profile': profile
    })

def bulk_delete_tasks(request):
    if request.method == 'POST':
        task_ids = request.POST.getlist('task_ids[]')
        Task.objects.filter(id__in=task_ids, user=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def bulk_update_tasks(request):
    if request.method == 'POST':
        task_ids = request.POST.getlist('task_ids[]')
        action = request.POST.get('action')
        
        if action == 'complete':
            Task.objects.filter(id__in=task_ids, user=request.user).update(complete=True)
        elif action == 'incomplete':
            Task.objects.filter(id__in=task_ids, user=request.user).update(complete=False)
            
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('login')

# Thêm middleware để kiểm tra user bị block trong mọi request
class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                if profile.is_blocked:
                    logout(request)
                    messages.error(request, "Tài khoản của bạn đã bị khóa.")
                    return redirect('login')
            except UserProfile.DoesNotExist:
                pass
        return self.get_response(request)

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user
        
        if not user.check_password(current_password):
            messages.error(request, 'Mật khẩu hiện tại không đúng!')
            return redirect('change_password')
            
        if len(new_password) < 8:
            messages.error(request, 'Mật khẩu mới phải có ít nhất 8 ký tự!')
            return redirect('change_password')
            
        if new_password != confirm_password:
            messages.error(request, 'Mật khẩu mới không khớp!')
            return redirect('change_password')
            
        # Cập nhật mật khẩu mới
        user.set_password(new_password)
        user.save()
        
        # Cập nhật session để user không bị logout
        update_session_auth_hash(request, user)
        messages.success(request, 'Đổi mật khẩu thành công!')
        return redirect('task')
        
    return render(request, 'blog/change_password.html')
