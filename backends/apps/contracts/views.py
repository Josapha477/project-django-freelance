from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Contract, Milestone, Payment, Review


@login_required
def contract_list(request):
    """List user's contracts."""
    profile = request.user.profile
    
    contracts = Contract.objects.filter(
        Q(client=profile) | Q(freelancer=profile)
    ).select_related('project', 'client', 'freelancer').order_by('-created_at')
    
    context = {
        'contracts': contracts,
    }
    return render(request, 'contracts/contract_list.html', context)


@login_required
def contract_detail(request, pk):
    """Contract detail view."""
    profile = request.user.profile
    
    contract = get_object_or_404(
        Contract.objects.select_related('project', 'client', 'freelancer', 'proposal'),
        Q(client=profile) | Q(freelancer=profile),
        pk=pk
    )
    
    milestones = contract.milestones.all()
    payments = contract.payments.all()
    reviews = contract.reviews.all()
    
    context = {
        'contract': contract,
        'milestones': milestones,
        'payments': payments,
        'reviews': reviews,
        'is_client': contract.client == profile,
        'is_freelancer': contract.freelancer == profile,
    }
    return render(request, 'contracts/contract_detail.html', context)


@login_required  
def complete_contract(request, pk):
    """Mark contract as completed."""
    profile = request.user.profile
    contract = get_object_or_404(Contract, pk=pk, client=profile, status=Contract.Status.ACTIVE)
    
    if request.method == 'POST':
        contract.status = Contract.Status.COMPLETED
        contract.save()
        
        # Update project status
        contract.project.status = contract.project.Status.COMPLETED
        contract.project.save()
        
        # Update freelancer stats
        freelancer = contract.freelancer.freelancer
        freelancer.completed_jobs += 1
        freelancer.total_earned += contract.total_amount
        freelancer.save()
        
        messages.success(request, 'Contrat termine avec succes!')
        return redirect('contracts:review', pk=pk)
    
    return redirect('contracts:detail', pk=pk)


@login_required
def review_contract(request, pk):
    """Leave a review for completed contract."""
    profile = request.user.profile
    contract = get_object_or_404(
        Contract,
        Q(client=profile) | Q(freelancer=profile),
        pk=pk,
        status=Contract.Status.COMPLETED
    )
    
    # Check if already reviewed
    if contract.reviews.filter(reviewer=profile).exists():
        messages.info(request, 'Vous avez deja laisse un avis.')
        return redirect('contracts:detail', pk=pk)
    
    if request.method == 'POST':
        reviewee = contract.freelancer if contract.client == profile else contract.client
        
        review = Review.objects.create(
            contract=contract,
            reviewer=profile,
            reviewee=reviewee,
            rating=int(request.POST.get('rating', 5)),
            comment=request.POST.get('comment', ''),
            communication_score=int(request.POST.get('communication', 5)),
            quality_score=int(request.POST.get('quality', 5)),
            deadline_score=int(request.POST.get('deadline', 5)),
        )
        
        # Update freelancer rating
        if hasattr(reviewee, 'freelancer'):
            freelancer = reviewee.freelancer
            all_reviews = Review.objects.filter(reviewee=reviewee)
            avg_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
            freelancer.rating_avg = round(avg_rating, 2)
            freelancer.save()
        
        messages.success(request, 'Merci pour votre avis!')
        return redirect('contracts:detail', pk=pk)
    
    return render(request, 'contracts/review_form.html', {'contract': contract})
