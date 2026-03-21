from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Conversation, Message


@login_required
def conversation_list(request):
    """List user's conversations."""
    profile = request.user.profile
    conversations = Conversation.objects.filter(
        participants=profile
    ).prefetch_related('participants', 'messages').order_by('-updated_at')
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'messaging/conversation_list.html', context)


@login_required
def conversation_detail(request, pk):
    """View conversation and send messages."""
    profile = request.user.profile
    conversation = get_object_or_404(
        Conversation.objects.prefetch_related('participants', 'messages'),
        participants=profile,
        pk=pk
    )
    
    # Mark messages as read
    conversation.messages.exclude(sender=profile).filter(read_at__isnull=True).update(
        read_at=timezone.now()
    )
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=profile,
                content=content
            )
            conversation.save()  # Update updated_at
            return redirect('messaging:detail', pk=pk)
    
    messages = conversation.messages.select_related('sender', 'sender__user').all()
    other_participant = conversation.participants.exclude(pk=profile.pk).first()
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'other_participant': other_participant,
    }
    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def start_conversation(request, user_pk):
    """Start a new conversation with a user."""
    from apps.accounts.models import UserProfile
    
    profile = request.user.profile
    other_user = get_object_or_404(UserProfile, pk=user_pk)
    
    if other_user == profile:
        return redirect('messaging:list')
    
    # Check if conversation already exists
    existing = Conversation.objects.filter(
        participants=profile
    ).filter(
        participants=other_user
    ).first()
    
    if existing:
        return redirect('messaging:detail', pk=existing.pk)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(profile, other_user)
    
    return redirect('messaging:detail', pk=conversation.pk)
