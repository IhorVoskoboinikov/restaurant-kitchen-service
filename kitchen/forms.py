from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Cook, Dish


class BaseCookForm(forms.ModelForm):
    MIN_EXPERIENCE = 0
    MAX_EXPERIENCE = 50

    class Meta:
        model = Cook
        fields = (
            "first_name",
            "last_name",
            "years_of_experience"
        )

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data.get("years_of_experience")

        if not BaseCookForm.MIN_EXPERIENCE <= years_of_experience < BaseCookForm.MAX_EXPERIENCE:
            raise ValidationError(
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


class CookSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by username:"
        })
    )


class DishSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name:"
        })
    )


class DishTypeSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Search by name:"
        })
    )
