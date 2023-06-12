from django import forms
from .models import Recipe, UserProfile, Category, Photo


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'category']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['category'].widget = forms.Select(choices=Category.objects.all())


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'favorite_category', 'social_facebook', 'social_twitter', 'social_instagram', 'social_tiktok']
