from django import forms
from .models import Project, Proposal
from apps.freelancers.models import Skill


class ProjectForm(forms.ModelForm):
    """Form for creating/updating projects."""
    skills_required = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 rounded'
        })
    )

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'budget_type', 'budget_min', 'budget_max',
            'duration', 'deadline', 'visibility', 'skills_required'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Titre du projet'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'rows': 6,
                'placeholder': 'Decrivez votre projet en detail...'
            }),
            'budget_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent'
            }),
            'budget_min': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Budget minimum en HTG'
            }),
            'budget_max': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Budget maximum en HTG'
            }),
            'duration': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'type': 'date'
            }),
            'visibility': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent'
            }),
        }


class ProposalForm(forms.ModelForm):
    """Form for submitting proposals."""
    class Meta:
        model = Proposal
        fields = ['cover_letter', 'bid_amount', 'estimated_duration']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'rows': 6,
                'placeholder': 'Expliquez pourquoi vous etes le bon freelancer pour ce projet...'
            }),
            'bid_amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Votre prix en HTG'
            }),
            'estimated_duration': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-transparent',
                'placeholder': 'Nombre de jours',
                'min': 1
            }),
        }
