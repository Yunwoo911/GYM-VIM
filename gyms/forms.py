from django import forms
from .models import PersonalInfo
from .models import TrainerRequest, Gym, Trainer


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = [
            'height', 'weight', 'medical_conditions', 'medications', 'frequency', 'types', 'intensity', 'goals',
            'diet_habits', 'sleep_pattern', 'stress_level', 'smoking', 'smoking_amount', 'drinking', 'drinking_amount',
            'body_fat_percentage', 'muscle_mass', 'basal_metabolic_rate', 'bmi', 'short_term_goals', 'long_term_goals',
            'preferred_exercise_types', 'available_times'
        ]
        widgets = {
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'medical_conditions': forms.TextInput(attrs={'class': 'form-control'}),
            'medications': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.NumberInput(attrs={'class': 'form-control'}),
            'types': forms.TextInput(attrs={'class': 'form-control'}),
            'intensity': forms.Select(attrs={'class': 'form-control'}, choices=[('low', '낮음'), ('medium', '보통'), ('high', '높음')]),
            'goals': forms.TextInput(attrs={'class': 'form-control'}),
            'diet_habits': forms.TextInput(attrs={'class': 'form-control'}),
            'sleep_pattern': forms.NumberInput(attrs={'class': 'form-control'}),
            'stress_level': forms.Select(attrs={'class': 'form-control'}, choices=[('low', '낮음'), ('medium', '보통'), ('high', '높음')]),
            'smoking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'smoking_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'drinking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'drinking_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'body_fat_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'muscle_mass': forms.NumberInput(attrs={'class': 'form-control'}),
            'basal_metabolic_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control'}),
            'short_term_goals': forms.TextInput(attrs={'class': 'form-control'}),
            'long_term_goals': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_exercise_types': forms.TextInput(attrs={'class': 'form-control'}),
            'available_times': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['gym', 'trainer_name', 'certificate', 'trainer_image']
        widgets = {
            'gym': forms.Select(attrs={'class': 'form-control'}),
            # 'user': forms.Select(attrs={'class': 'form-control'}),
            'trainer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'certificate': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class TrainerRequestForm(forms.ModelForm):
    class Meta:
        model = TrainerRequest
        fields = ['requested_gym', 'request_message']
        widgets = {
            'request_message': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
