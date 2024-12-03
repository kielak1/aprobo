from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, FormView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from .user_admin_form import CustomUserChangeForm, CustomPasswordChangeForm, ExtendedUserChangeForm
from general.models import Sections
from general.common_context import common_context

class IsUserAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='useradmin').exists()
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % (reverse('account_login'), self.request.path))
        else:
            return redirect('login')

class GroupRequiredMixin(AccessMixin):
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if self.group_required and not request.user.groups.filter(name=self.group_required).exists():
            return redirect(self.login_url)
        
        return super().dispatch(request, *args, **kwargs)

class UserListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    login_url = '/account/login/'
    redirect_field_name = 'redirect_to'
    group_required = 'useradmin'

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update( common_context( self.request) )
        return context    

class UserUpdateView(IsUserAdminMixin, UpdateView):
    model = User
    form_class = ExtendedUserChangeForm
    template_name = 'user_edit_form.html'
    success_url = reverse_lazy('user-list')  # Załóżmy, że tak nazwaliśmy URL do listy użytkowników

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update( common_context( self.request) )
        return context
        
    def get_initial(self):
        initial = super().get_initial()
        user = self.get_object()
        # Ustaw początkowe wartości dla sekcji na podstawie aktualnych przypisań użytkownika
        initial['sections'] = Sections.objects.filter(users=user).values_list('id', flat=True)
        return initial
    
    def form_valid(self, form):
        is_useradmin = self.object.groups.filter(name='useradmin').exists()
 
        response = super().form_valid(form)

        # Najpierw usuń użytkownika ze wszystkich sekcji
        self.object.custom_models.clear()
        # Następnie przypisz użytkownika do wybranych sekcji
        selected_sections = form.cleaned_data['sections']
        for section in selected_sections:
            section.users.add(self.object)  # Dodaj użytkownika do sekcji

        user = form.save(commit=False)

        new_password = form.cleaned_data.get('new_password1')
        if new_password:
            user.password = make_password(new_password)
        user.save()
        form.save_m2m()

        return response

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

class PasswordChangeView(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm  # lub użyj CustomPasswordChangeForm, jeśli istnieje
    template_name = 'pass_change_form.html'
    success_url = reverse_lazy('dashboard')
    login_url = '/account/login/'
    redirect_field_name = 'redirect_to'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Zapisanie nowego hasła
        form.save()
        update_session_auth_hash(self.request, form.user)  # Zapewnia, że użytkownik pozostaje zalogowany
        return super().form_valid(form)
