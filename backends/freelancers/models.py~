from django.db import models
from apps.accounts.models import BaseModel, UserProfile, Language


class SkillCategory(models.Model):
    """Categories for skills."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Skills that freelancers can have."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class FreelancerProfile(BaseModel):
    """Freelancer specific profile."""
    class Availability(models.TextChoices):
        AVAILABLE = 'available', 'Disponible'
        BUSY = 'busy', 'Occupe'
        UNAVAILABLE = 'unavailable', 'Indisponible'

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='freelancer')
    title = models.CharField(max_length=255, help_text="Ex: Developpeur Web Full Stack")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Taux horaire en HTG")
    availability = models.CharField(
        max_length=20, 
        choices=Availability.choices, 
        default=Availability.AVAILABLE
    )
    years_experience = models.PositiveIntegerField(default=0)
    portfolio_url = models.URLField(blank=True)
    
    languages = models.ManyToManyField(Language, blank=True)
    skills = models.ManyToManyField(Skill, through='FreelancerSkill', blank=True)
    
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    completed_jobs = models.PositiveIntegerField(default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"

    @property
    def display_rate(self):
        return f"{self.hourly_rate:,.0f} HTG/h"


class FreelancerSkill(models.Model):
    """Intermediate model for freelancer skills with level."""
    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Debutant'
        INTERMEDIATE = 'intermediate', 'Intermediaire'
        EXPERT = 'expert', 'Expert'

    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.INTERMEDIATE)

    class Meta:
        unique_together = ('freelancer', 'skill')

    def __str__(self):
        return f"{self.freelancer} - {self.skill} ({self.get_level_display()})"


class PortfolioItem(BaseModel):
    """Portfolio items for freelancers."""
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    url = models.URLField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return f"{self.title} - {self.freelancer}"
