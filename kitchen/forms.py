from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Cook, Dish


class BaseCookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = (
            "first_name",
            "last_name",
            "years_of_experience"
        )

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data.get("years_of_experience")

        if not 0 <= years_of_experience < 50:
            raise forms.ValidationError(
                "Year of experience must be between 0 and 50 years!"
            )

        return years_of_experience


class CookCreationForm(BaseCookForm, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + BaseCookForm.Meta.fields


class CookUpdateForm(BaseCookForm):
    pass


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"
