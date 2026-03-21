from django.db import models
from accounts.models import BaseModel, UserProfile
from projects.models import Project, Proposal


class Contract(BaseModel):
    """Contract between client and freelancer."""
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Actif'
        PAUSED = 'paused', 'En pause'
        COMPLETED = 'completed', 'Termine'
        DISPUTED = 'disputed', 'En litige'
        CANCELLED = 'cancelled', 'Annule'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contracts')
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE)
    
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_contracts')
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='freelancer_contracts')
    
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    terms = models.TextField(blank=True)

    def __str__(self):
        return f"Contrat: {self.project.title}"


class Milestone(BaseModel):
    """Milestones for contracts."""
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        IN_PROGRESS = 'in_progress', 'En cours'
        SUBMITTED = 'submitted', 'Soumis'
        APPROVED = 'approved', 'Approuve'
        PAID = 'paid', 'Paye'

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='milestones')
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.title} - {self.contract.project.title}"


class Payment(BaseModel):
    """Payment records."""
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        ESCROW = 'escrow', 'En depot'
        RELEASED = 'released', 'Libere'
        REFUNDED = 'refunded', 'Rembourse'

    class Method(models.TextChoices):
        MONCASH = 'moncash', 'MonCash'
        BANK = 'bank', 'Virement bancaire'
        CASH = 'cash', 'Especes'

    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payments')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=50, choices=Method.choices, default=Method.MONCASH)
    
    moncash_transaction_id = models.CharField(max_length=255, blank=True)
    
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Paiement {self.amount} HTG - {self.contract}"


class Review(BaseModel):
    """Reviews for completed contracts."""
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='reviews')
    
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_reviews')
    
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True)
    
    communication_score = models.PositiveSmallIntegerField(default=5)
    quality_score = models.PositiveSmallIntegerField(default=5)
    deadline_score = models.PositiveSmallIntegerField(default=5)
    
    is_public = models.BooleanField(default=True)

    class Meta:
        unique_together = ('contract', 'reviewer')

    def __str__(self):
        return f"Avis de {self.reviewer} pour {self.reviewee}"
