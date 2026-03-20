from django import forms
from .models import FreelancerProfile, Skill, PortfolioItem


class FreelancerProfileForm(forms.ModelForm):
    """Form for creating/updating freelancer profile."""
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 rounded'
        })
    )

    class Meta:
        model = FreelancerProfile
        fields = ['title', 'hourly_rate', 'availability', 'years_experience', 'portfolio_url', 'languages']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Ex: Developpeur Web Full Stack'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Taux horaire en HTG'
            }),
            'availability': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent'
            }),
            'years_experience': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'min': 0
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'https://votre-portfolio.com'
            }),
            'languages': forms.CheckboxSelectMultiple(attrs={
                'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 rounded'
            }),
        }


class PortfolioItemForm(forms.ModelForm):
    """Form for portfolio items."""
    class Meta:
        model = PortfolioItem
        fields = ['title', 'description', 'image', 'url', 'skills']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'rows': 4
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
            }),
            'skills': forms.CheckboxSelectMultiple(attrs={
                'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 rounded'
            }),
        }
