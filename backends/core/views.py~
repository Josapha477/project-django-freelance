from django.shortcuts import render
from apps.freelancers.models import FreelancerProfile, SkillCategory
from apps.projects.models import Project


def home(request):
    """Landing page view."""
    featured_freelancers = FreelancerProfile.objects.filter(
        user__is_verified=True
    ).order_by('-rating_avg')[:6]
    
    categories = SkillCategory.objects.all()[:8]
    
    recent_projects = Project.objects.filter(
        status=Project.Status.OPEN,
        visibility=Project.Visibility.PUBLIC
    ).order_by('-created_at')[:6]
    
    # Stats
    stats = {
        'freelancers_count': FreelancerProfile.objects.count(),
        'projects_count': Project.objects.filter(status=Project.Status.COMPLETED).count(),
        'active_projects': Project.objects.filter(status=Project.Status.OPEN).count(),
    }
    
    context = {
        'featured_freelancers': featured_freelancers,
        'categories': categories,
        'recent_projects': recent_projects,
        'stats': stats,
    }
    return render(request, 'core/home.html', context)
