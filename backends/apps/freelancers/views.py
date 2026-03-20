from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import FreelancerProfile, SkillCategory, Skill


def freelancer_list(request):
    """List all freelancers with filters."""
    freelancers = FreelancerProfile.objects.select_related('user', 'user__user').all()
    
    # Filters
    category = request.GET.get('category')
    skill = request.GET.get('skill')
    availability = request.GET.get('availability')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    search = request.GET.get('q')
    
    if category:
        freelancers = freelancers.filter(skills__category__slug=category)
    
    if skill:
        freelancers = freelancers.filter(skills__slug=skill)
    
    if availability:
        freelancers = freelancers.filter(availability=availability)
    
    if min_rate:
        freelancers = freelancers.filter(hourly_rate__gte=min_rate)
    
    if max_rate:
        freelancers = freelancers.filter(hourly_rate__lte=max_rate)
    
    if search:
        freelancers = freelancers.filter(
            Q(title__icontains=search) |
            Q(user__user__first_name__icontains=search) |
            Q(user__user__last_name__icontains=search) |
            Q(skills__name__icontains=search)
        ).distinct()
    
    # Ordering
    order = request.GET.get('order', '-rating_avg')
    freelancers = freelancers.order_by(order)
    
    # Pagination
    paginator = Paginator(freelancers, 12)
    page = request.GET.get('page', 1)
    freelancers = paginator.get_page(page)
    
    context = {
        'freelancers': freelancers,
        'categories': SkillCategory.objects.all(),
        'skills': Skill.objects.all(),
        'current_filters': {
            'category': category,
            'skill': skill,
            'availability': availability,
            'min_rate': min_rate,
            'max_rate': max_rate,
            'search': search,
            'order': order,
        }
    }
    return render(request, 'freelancers/freelancer_list.html', context)


def freelancer_detail(request, pk):
    """Freelancer profile detail view."""
    freelancer = get_object_or_404(
        FreelancerProfile.objects.select_related('user', 'user__user'),
        pk=pk
    )
    
    # Get reviews
    from apps.contracts.models import Review
    reviews = Review.objects.filter(
        reviewee=freelancer.user,
        is_public=True
    ).select_related('reviewer', 'reviewer__user').order_by('-created_at')[:10]
    
    # Get portfolio items
    portfolio = freelancer.portfolio_items.all()
    
    # Get skills with levels
    skills = freelancer.freelancerskill_set.select_related('skill', 'skill__category').all()
    
    context = {
        'freelancer': freelancer,
        'reviews': reviews,
        'portfolio': portfolio,
        'skills': skills,
    }
    return render(request, 'freelancers/freelancer_detail.html', context)
