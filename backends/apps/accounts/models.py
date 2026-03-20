from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """Base model with timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    """Extended user profile."""
    class Role(models.TextChoices):
        CLIENT = 'client', 'Client'
        FREELANCER = 'freelancer', 'Freelancer'
        BOTH = 'both', 'Les deux'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=100, default='America/Port-au-Prince')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def is_freelancer(self):
        return self.role in [self.Role.FREELANCER, self.Role.BOTH]

    @property
    def is_client(self):
        return self.role in [self.Role.CLIENT, self.Role.BOTH]


class Language(models.Model):
    """Languages spoken by users."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Notification(BaseModel):
    """User notifications."""
    class Type(models.TextChoices):
        PROPOSAL = 'proposal', 'Proposition'
        MESSAGE = 'message', 'Message'
        PAYMENT = 'payment', 'Paiement'
        REVIEW = 'review', 'Avis'
        CONTRACT = 'contract', 'Contrat'
        SYSTEM = 'system', 'Systeme'

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=Type.choices)
    title = models.CharField(max_length=255)
    body = models.TextField()
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user}"
