from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from kitchen.models import DishType, Dish
from kitchen.forms import (
    DishTypeSearchForm,
    DishSearchForm,
    CookSearchForm
)


class PublicDriverViewsTest(TestCase):
    def test_login_required_dish_type_list_view(self):
        dish_type_list_url = reverse("kitchen:dish-type-list")
        response = self.client.get(dish_type_list_url)

        self.assertNotEquals(response.status_code, 200)

    def test_login_required_dish_list_view(self):
        dish_list_url = reverse("kitchen:dish-list")
        response = self.client.get(dish_list_url)

        self.assertNotEquals(response.status_code, 200)

    def test_login_required_driver_list_view(self):
        cook_list_url = reverse("kitchen:cook-list")
        response = self.client.get(cook_list_url)

        self.assertNotEquals(response.status_code, 200)


class PrivateDriverViewsTest(TestCase):
    def setUp(self):
        self.pagination = 5
        self.pagination_data = (
            {
                "view_name": "kitchen:dish-list",
                "response_context": "dish_list"
            },
            {
                "view_name": "kitchen:dish-type-list",
                "response_context": "dish_type_list"
            },
            {
                "view_name": "kitchen:cook-list",
                "response_context": "cook_list"
            },
        )
        for num in range(8):
            get_user_model().objects.create_user(
                username=f"testusername{num}",
                first_name=f"First name Test{num}",
                last_name=f"Last name Test{num}",
                password=f"123testadmin{num}",
                years_of_experience=num
            )

        self.client.force_login(get_user_model().objects.get(id=1))

        for num in range(8):
            DishType.objects.create(
                name=f"dish-type-test#{num}",
            )
        for dish_num in range(8):
            Dish.objects.create(
                name=f"Test dish#{dish_num}",
                description="Test description",
                price="1.25",
                dish_type=DishType.objects.get(id=1)
            )

    def test_retrieve_dish_list(self):
        dish_list_url = reverse("kitchen:dish-list")
        response = self.client.get(dish_list_url)

        cars = Dish.objects.all()[:5]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["dish_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_retrieve_dish_type_list(self):
        dish_type_list_url = reverse("kitchen:dish-type-list")
        response = self.client.get(dish_type_list_url)

        manufacturer = DishType.objects.all()[:5]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["dish_type_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_create_author_in_db(self):
        form_data = {
            "username": "test",
            "first_name": "First name Test",
            "last_name": "Last name Test",
            "password1": "123testadmin",
            "password2": "123testadmin",
            "years_of_experience": 10
        }

        self.client.post(reverse("kitchen:cook-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(
            new_user.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_user.last_name,
            form_data["last_name"]
        )
        self.assertEqual(
            new_user.years_of_experience,
            form_data["years_of_experience"]
        )

    def test_all_list_pagination_is_five(self):
        for pagination in self.pagination_data:
            response = self.client.get(reverse(pagination["view_name"]))
            self.assertEqual(response.status_code, 200)
            self.assertTrue("is_paginated" in response.context)
            self.assertTrue(response.context["is_paginated"] is True)
            self.assertEqual(
                len(
                    response.context[pagination["response_context"]]
                ),
                self.pagination)

    def test_search_dish_type_using_form(self):
        DishType.objects.create(name="Pizza")

        response = self.client.get(
            reverse("kitchen:dish-type-list"), {"title": "Pizza"}
        )
        form = DishTypeSearchForm({"title": "Pizza"})
        expected_queryset = DishType.objects.filter(
            name__icontains="Pizza"
        )

        self.assertTrue(form.is_valid())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["dish_type_list"]),
            list(expected_queryset)
        )

    def test_search_dish_using_form(self):
        Dish.objects.create(
            name="Margarita",
            description="Test description",
            price="10.50",
            dish_type=DishType.objects.get(id=1)
        )

        response = self.client.get(
            reverse("kitchen:dish-list"), {"title": "Margarita"}
        )
        form = DishSearchForm({"title": "Margarita"})
        expected_queryset = Dish.objects.select_related(
            "dish_type"
        ).filter(name__icontains="Margarita")

        self.assertTrue(form.is_valid())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["dish_list"]),
            list(expected_queryset)
        )

    def test_search_cook_using_form(self):
        get_user_model().objects.create_user(
            username="UserForTest",
            password="123testadmin123",

        )

        response = self.client.get(
            reverse("kitchen:cook-list"), {"title": "UserForTest"}
        )
        form = CookSearchForm({"title": "UserForTest"})
        expected_queryset = get_user_model().objects.filter(
            username__icontains="UserForTest")

        self.assertTrue(form.is_valid())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["cook_list"]),
            list(expected_queryset)
        )
