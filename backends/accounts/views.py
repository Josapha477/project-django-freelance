from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, UserProfileForm
from .models import UserProfile


class CustomLoginView(LoginView):
    """Custom login view."""
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = reverse_lazy('core:home')


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Bienvenue sur FreelanceHT!')
            
            # Redirect based on role
            if form.cleaned_data['role'] == UserProfile.Role.FREELANCER:
                return redirect('accounts:complete_freelancer_profile')
            return redirect('accounts:dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard view - redirects to appropriate dashboard."""
    profile = request.user.profile
    
    if profile.is_freelancer:
        return redirect('accounts:freelancer_dashboard')
    return redirect('accounts:client_dashboard')


@login_required
def freelancer_dashboard(request):
    """Freelancer dashboard view."""
    profile = request.user.profile
    
    if not profile.is_freelancer:
        messages.error(request, 'Vous devez etre freelancer pour acceder a cette page.')
        return redirect('accounts:client_dashboard')
    
    freelancer = getattr(profile, 'freelancer', None)
    
    context = {
        'profile': profile,
        'freelancer': freelancer,
        'active_contracts': [],
        'pending_proposals': [],
        'recent_messages': [],
    }
    
    if freelancer:
        from contracts.models import Contract
        from projects.models import Proposal
        
        context['active_contracts'] = Contract.objects.filter(
            freelancer=profile,
            status=Contract.Status.ACTIVE
        )[:5]
        
        context['pending_proposals'] = Proposal.objects.filter(
            freelancer=freelancer,
            status=Proposal.Status.PENDING
        )[:5]
    
    return render(request, 'accounts/dashboard_freelancer.html', context)


@login_required
def client_dashboard(request):
    """Client dashboard view."""
    profile = request.user.profile
    
    from projects.models import Project, Proposal
    from contracts.models import Contract
    
    context = {
        'profile': profile,
        'my_projects': Project.objects.filter(client=profile).order_by('-created_at')[:5],
        'active_contracts': Contract.objects.filter(
            client=profile,
            status=Contract.Status.ACTIVE
        )[:5],
        'pending_proposals': Proposal.objects.filter(
            project__client=profile,
            status=Proposal.Status.PENDING
        )[:10],
    }
    
    return render(request, 'accounts/dashboard_client.html', context)


@login_required
def profile(request):
    """View and edit user profile."""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            form.save()
            messages.success(request, 'Profil mis a jour avec succes!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


@login_required
def complete_freelancer_profile(request):
    """Complete freelancer profile after registration."""
    from freelancers.forms import FreelancerProfileForm
    
    profile = request.user.profile
    
    # Check if already has freelancer profile
    if hasattr(profile, 'freelancer'):
        return redirect('accounts:freelancer_dashboard')
    
    if request.method == 'POST':
        form = FreelancerProfileForm(request.POST)
        if form.is_valid():
            freelancer = form.save(commit=False)
            freelancer.user = profile
            freelancer.save()
            form.save_m2m()
            messages.success(request, 'Profil freelancer complete!')
            return redirect('accounts:freelancer_dashboard')
    else:
        form = FreelancerProfileForm()
    
    return render(request, 'accounts/complete_freelancer_profile.html', {'form': form})
