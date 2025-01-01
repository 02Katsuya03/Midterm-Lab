from django.shortcuts import render, redirect,  get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, FormView, UpdateView, DeleteView, View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import RegistrationUserForm, LoginUserForm, LoginAdminForm, LostItemForm, FoundItemForm
from .models import Profile, LostItem, School, HistoryLog, FoundItem, F2FClaim, OnlineClaim
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Q
from datetime import timedelta
from django.utils.timezone import now

def logout_view(request):
    logout(request)
    return redirect('intro')

class RegisterUserView(FormView):
    template_name = 'app/register_user.html'
    form_class = RegistrationUserForm
    success_url = reverse_lazy('intro')

    def form_valid(self, form):
        
        user = form.save()

        
        Profile.objects.create(
            user=user,
            middle_name=form.cleaned_data['middle_name'],
            sex=form.cleaned_data['sex'],
            phone_number=form.cleaned_data['phone_number'],
            school=form.cleaned_data['school'],
            role='USER'  
        )

        
        login(self.request, user)

        
        messages.success(self.request, "Registration successful! You are now logged in.")

        
        return redirect('intro')

class RegisterAdminView(FormView):
    template_name = 'app/register_admin.html'
    form_class = RegistrationUserForm
    success_url = reverse_lazy('intro')

    def form_valid(self, form):
        
        user = form.save()

        
        Profile.objects.create(
            user=user,
            middle_name=form.cleaned_data['middle_name'],
            sex=form.cleaned_data['sex'],
            phone_number=form.cleaned_data['phone_number'],
            school=form.cleaned_data['school'],
            role='ADMIN'  
        )

        
        login(self.request, user)

        
        messages.success(self.request, "Registration successful! You are now logged in as an admin.")

        
        return redirect('intro')


class LoginUserView(FormView):
    template_name = 'app/login_user.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('user')  

    def form_valid(self, form):
        
        user = form.get_user()
        role = form.cleaned_data['role']  
        school_id = form.cleaned_data['school']
        
        try:
            
            profile = Profile.objects.get(user=user)
            
            
            if profile.role.lower() != role.lower():  
                messages.error(self.request, f"Incorrect role. Expected {profile.role}, but got {role}.")
                return redirect('login_user')

            
            if profile.school.id != int(school_id):  
                messages.error(self.request, "User does not belong to this school.")
                return redirect('login_user')
            
            
            login(self.request, user)

            
            messages.success(self.request, "Login successful! Welcome to your dashboard.")

            
            return super().form_valid(form)

        except Profile.DoesNotExist:
            messages.error(self.request, "No profile associated with this user.")
            return redirect('login_user')  

class LoginAdminView(FormView):
    template_name = 'app/login_admin.html'
    form_class = LoginAdminForm
    success_url = reverse_lazy('administrator')  

    def form_valid(self, form):
        
        user = form.get_user()
        school_id = form.cleaned_data['school']
        
        try:
            profile = Profile.objects.get(user=user)
            
            
            if profile.role.lower() != 'admin':  
                messages.error(self.request, "You cannot access this; it is for admin only.")
                return redirect('login_user')

            
            if profile.school.id != int(school_id):  
                messages.error(self.request, "Admin does not belong to this school.")
                return redirect('login_user')
            
            
            login(self.request, user)
            
            
            return super().form_valid(form)

        except Profile.DoesNotExist:
            messages.error(self.request, "No profile associated with this user.")
            return redirect('login_user')  

class IntroPageView(TemplateView):
    template_name = 'app/intro.html'

class LoginBasePageView(TemplateView):
    template_name = 'app/login_base.html'


class AdminPageView(TemplateView):
    template_name = 'app/administrator.html'


class UserPageView(TemplateView):
    template_name = 'app/user.html'


class LostView(TemplateView):
    template_name = 'app/lost.html'

class LostDashboardView(ListView):
    template_name = 'app/lost_dashboard.html'
    model = LostItem
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        context['total_users'] = User.objects.exclude(is_superuser=True).count()
        context['total_lost_items'] = LostItem.objects.count()
        context['total_found_items'] = FoundItem.objects.count()
        context['total_claims'] = F2FClaim.objects.count() + OnlineClaim.objects.count()
        
        
        recent_days = 7
        recent_date = now() - timedelta(days=recent_days)
        context['recent_items'] = LostItem.objects.filter(date_added__gte=recent_date).order_by('-date_added')

        return context
    
    def is_new(self, item):
        """Returns True if the item was created today."""
        return item.created_at.date() == date.today()

class LostSchool(TemplateView):
    template_name = 'app/lost_school.html'

class LostSchoolListView(ListView):
    model = LostSchool
    template_name = 'app/lost_school.html'  
    context_object_name = 'schools'

class LostListView(ListView):
    template_name = 'app/lost_listview.html'
    model = LostItem
    context_object_name = 'items'
    paginate_by = 15
    queryset = LostItem.objects.all()

    def get_queryset(self):
        
        queryset = LostItem.objects.all()

        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(item_name__icontains=query) | Q(item_id__icontains=query)
            )

        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        
        school_id = self.request.GET.get('school')
        if school_id:
            queryset = queryset.filter(school_id=school_id)

        
        order_by = self.request.GET.get('order_by', 'desc')  
        if order_by == 'asc':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LostItem.objects.values_list('category', flat=True).distinct()
        context['schools'] = School.objects.all()  
        context['today'] = date.today()  
        return context
    
    def is_new(self, item):
        """Returns True if the item was created today."""
        return item.created_at.date() == date.today()
    

class LostViewItem(ListView):
    template_name = 'app/lost_viewitem.html'
    model = LostItem
    context_object_name = 'items'
    paginate_by = 20
    
    def get_queryset(self):
        
        queryset = LostItem.objects.all()

        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(item_name__icontains=query) | Q(item_id__icontains=query)
            )

        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        
        school_id = self.request.GET.get('school')
        if school_id:
            queryset = queryset.filter(school_id=school_id)

        
        order_by = self.request.GET.get('order_by', 'desc')  
        if order_by == 'asc':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LostItem.objects.values_list('category', flat=True).distinct()
        context['schools'] = School.objects.all()  
        context['today'] = date.today()  
        return context
    
    def is_new(self, item):
        """Returns True if the item was created today."""
        return item.created_at.date() == date.today()
    

class LostDetailView(DetailView):
    model = LostItem
    template_name = 'app/lost_detailview.html'  
    context_object_name = 'item'

    def get_object(self, queryset=None):
        
        item_id = self.kwargs.get('item_id')  
        return LostItem.objects.get(item_id=item_id)



class LostAddItemView(CreateView):
    model = LostItem
    form_class = LostItemForm  
    template_name = 'app/lost_additem.html'
    success_url = reverse_lazy('lost_listview')

    def form_valid(self, form):
        
        if not form.instance.item_id:
            form.instance.item_id = form.instance._generate_unique_item_id()
        
        
        response = super().form_valid(form)        
        return response
    
    def form_valid(self, form):
        if not form.instance.item_id:
            form.instance.item_id = form.instance._generate_unique_item_id()
        
        response = super().form_valid(form)

        return response
    
class LostUpdateItemView(UpdateView):
    model = LostItem
    fields = ['item_name', 'description', 'category', 'location_lost', 'lost_by', 'contact_information', 'photo', 'school']
    template_name = 'app/lost_updateitem.html'
    success_url = reverse_lazy('lost_listview')  

    def get_object(self, queryset=None):
        
        return get_object_or_404(LostItem, item_id=self.kwargs['item_id'])
    
class LostDeleteItemView(DeleteView):
    model = LostItem
    success_url = reverse_lazy('lost_listview')  

    def get_object(self, queryset=None):
        
        return get_object_or_404(LostItem, item_id=self.kwargs['item_id'])
    
    def delete(self, request, *args, **kwargs):
        item = self.get_object()

        
        profile = self.request.user.profile  
        HistoryLog.objects.create(
            action='delete',
            item_name=item.item_name,
            item_id=item.id,
            performed_by=f"{self.request.user.first_name} {self.request.user.last_name}",
            role=profile.role,
            school=profile.school
        )

        return super().delete(request, *args, **kwargs)

class FoundView(TemplateView):
    template_name = 'app/found.html'

class FoundDashboardView(ListView):
    template_name = 'app/found_dashboard.html'
    model = FoundItem
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        context['total_users'] = User.objects.exclude(is_superuser=True).count()
        context['total_found_items'] = FoundItem.objects.count()
        context['total_lost_items'] = LostItem.objects.count()
        context['total_claims'] = F2FClaim.objects.count() + OnlineClaim.objects.count()
        
        
        recent_days = 7
        recent_date = now() - timedelta(days=recent_days)
        context['recent_items'] = FoundItem.objects.filter(date_added__gte=recent_date).order_by('-date_added')

        return context
    
    def is_new(self, item):
        """Returns True if the item was created today."""
        return item.created_at.date() == date.today()

class FoundListView(ListView):
    template_name = 'app/found_listview.html'
    model = FoundItem
    context_object_name = 'items'
    paginate_by = 15
    queryset =FoundItem.objects.all()

    def get_queryset(self):
        
        queryset = FoundItem.objects.all()

        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(item_name__icontains=query) | Q(item_id__icontains=query)
            )

        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        
        school_id = self.request.GET.get('school')
        if school_id:
            queryset = queryset.filter(school_id=school_id)

        
        order_by = self.request.GET.get('order_by', 'desc')  
        if order_by == 'asc':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FoundItem.objects.values_list('category', flat=True).distinct()
        context['schools'] = School.objects.all()  
        context['today'] = date.today()  
        return context
    
    def is_new(self, item):
        """Returns True if the item was created today."""
        return item.created_at.date() == date.today()
    

class FoundViewItem(ListView):
    template_name = 'app/found_viewitem.html'
    model = FoundItem
    context_object_name = 'items'
    paginate_by = 20
    
    def get_queryset(self):
        
        queryset = FoundItem.objects.all()

        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(item_name__icontains=query) | Q(item_id__icontains=query)
            )

        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        
        school_id = self.request.GET.get('school')
        if school_id:
            queryset = queryset.filter(school_id=school_id)

        
        order_by = self.request.GET.get('order_by', 'desc')  
        if order_by == 'asc':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FoundItem.objects.values_list('category', flat=True).distinct()
        context['schools'] = School.objects.all()  
        context['today'] = date.today()  
        return context
    
    def is_new(self, item):
        """Returns True if the item was created today."""
        return item.created_at.date() == date.today()
    

class FoundDetailView(DetailView):
    model = LostItem
    template_name = 'app/found_detailview.html'  
    context_object_name = 'item'

    def get_object(self, queryset=None):
        
        item_id = self.kwargs.get('item_id')  
        return FoundItem.objects.get(item_id=item_id)



class FoundAddItemView(CreateView):
    model = FoundItem
    form_class = FoundItemForm  
    template_name = 'app/found_additem.html'
    success_url = reverse_lazy('found_listview')

    def form_valid(self, form):
        
        if not form.instance.item_id:
            form.instance.item_id = form.instance._generate_unique_item_id()
        
        
        response = super().form_valid(form)        
        return response
    
    def form_valid(self, form):
        if not form.instance.item_id:
            form.instance.item_id = form.instance._generate_unique_item_id()
        
        response = super().form_valid(form)

        return response
    
class FoundUpdateItemView(UpdateView):
    model = FoundItem
    fields = ['item_name', 'description', 'category', 'location_found', 'found_by', 'contact_information', 'photo', 'school']
    template_name = 'app/found_updateitem.html'
    success_url = reverse_lazy('found_listview')  

    def get_object(self, queryset=None):
        
        return get_object_or_404(FoundItem, item_id=self.kwargs['item_id'])
    
class FoundDeleteItemView(DeleteView):
    model = FoundItem
    success_url = reverse_lazy('found_listview')  

    def get_object(self, queryset=None):
        
        return get_object_or_404(FoundItem, item_id=self.kwargs['item_id'])
    
    def delete(self, request, *args, **kwargs):
        item = self.get_object()

        
        profile = self.request.user.profile  
        HistoryLog.objects.create(
            action='delete',
            item_name=item.item_name,
            item_id=item.id,
            performed_by=f"{self.request.user.first_name} {self.request.user.last_name}",
            role=profile.role,
            school=profile.school
        )

        return super().delete(request, *args, **kwargs)

class ClaimView(TemplateView):
    template_name = 'app/claim.html'



