from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cook, Dish, DishType
from .forms import (
    CookCreationForm,
    CookUpdateForm,
    DishForm,
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm
)


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
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

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(CookListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = CookSearchForm(initial={
            "title": title
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Cook.objects.all()

        form = CookSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["title"])
        return queryset


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


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(DishTypeListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = DishTypeSearchForm(initial={
            "title": title
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = DishType.objects.all()

        form = DishTypeSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["title"])
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(DishListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = DishSearchForm(initial={
            "title": title
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Dish.objects.select_related("dish_type")

        form = DishSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["title"])
        return queryset


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class CookAssignToDish(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        cook = get_object_or_404(Cook, id=request.user.id)
        dish = get_object_or_404(Dish, id=pk)

        if dish in cook.dishes.all():
            cook.dishes.remove(dish)
        else:
            cook.dishes.add(dish)

        return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))
