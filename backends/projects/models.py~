from django.db import models
from apps.accounts.models import BaseModel, UserProfile
from apps.freelancers.models import FreelancerProfile, Skill


class Project(BaseModel):
    """Project posted by clients."""
    class BudgetType(models.TextChoices):
        FIXED = 'fixed', 'Prix fixe'
        HOURLY = 'hourly', 'Taux horaire'

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        OPEN = 'open', 'Ouvert'
        IN_PROGRESS = 'in_progress', 'En cours'
        COMPLETED = 'completed', 'Termine'
        CANCELLED = 'cancelled', 'Annule'

    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Public'
        PRIVATE = 'private', 'Prive'
        INVITE_ONLY = 'invite_only', 'Sur invitation'

    class Duration(models.TextChoices):
        LESS_WEEK = 'less_week', 'Moins d\'une semaine'
        ONE_TWO_WEEKS = 'one_two_weeks', '1-2 semaines'
        TWO_FOUR_WEEKS = 'two_four_weeks', '2-4 semaines'
        ONE_THREE_MONTHS = 'one_three_months', '1-3 mois'
        THREE_SIX_MONTHS = 'three_six_months', '3-6 mois'
        MORE_SIX_MONTHS = 'more_six_months', 'Plus de 6 mois'

    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    budget_type = models.CharField(max_length=10, choices=BudgetType.choices, default=BudgetType.FIXED)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    duration = models.CharField(max_length=20, choices=Duration.choices, blank=True)
    deadline = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    
    skills_required = models.ManyToManyField(Skill, blank=True, related_name='projects')
    
    expires_at = models.DateTimeField(null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def budget_display(self):
        if self.budget_min and self.budget_max:
            return f"{self.budget_min:,.0f} - {self.budget_max:,.0f} HTG"
        elif self.budget_min:
            return f"A partir de {self.budget_min:,.0f} HTG"
        elif self.budget_max:
            return f"Jusqu'a {self.budget_max:,.0f} HTG"
        return "A discuter"

    @property
    def proposals_count(self):
        return self.proposals.count()


class Proposal(BaseModel):
    """Proposal from freelancer for a project."""
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        ACCEPTED = 'accepted', 'Accepte'
        REJECTED = 'rejected', 'Rejete'
        WITHDRAWN = 'withdrawn', 'Retire'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='proposals')
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='proposals')
    
    cover_letter = models.TextField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.PositiveIntegerField(help_text="Duree estimee en jours")
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        unique_together = ('project', 'freelancer')
        ordering = ['-created_at']

    def __str__(self):
        return f"Proposition de {self.freelancer} pour {self.project}"


class File(BaseModel):
    """File attachments."""
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='attachments/')
    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
