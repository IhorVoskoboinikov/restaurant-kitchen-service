from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CookCreationForm, CookUpdateForm
from .models import Cook, Dish, DishType


@login_required
def index(request):
    """View function for the home page of the site."""

    total_chefs = Cook.objects.count()
    total_dish_type = Dish.objects.count()
    total_dish = DishType.objects.count()

    context = {
        "total_chefs": total_chefs,
        "total_dish_type": total_dish_type,
        "total_dish": total_dish,
    }

    return render(request, "kitchen/index.html", context=context)


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")
