from django.db import models
from accounts.models import BaseModel, UserProfile
from projects.models import Project


class Conversation(BaseModel):
    """Conversation between users."""
    participants = models.ManyToManyField(UserProfile, related_name='conversations')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Conversation #{self.pk}"

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()


class Message(BaseModel):
    """Messages in a conversation."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    content = models.TextField()
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message de {self.sender} - {self.content[:50]}"
