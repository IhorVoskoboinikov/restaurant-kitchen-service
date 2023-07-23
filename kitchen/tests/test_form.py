from django.test import TestCase

from kitchen.forms import (
    DishTypeSearchForm,
    DishSearchForm,
    CookSearchForm,
    CookUpdateForm,
    CookCreationForm,
)


class FormTest(TestCase):
    def test_cook_create_with_clean_years_of_experience_is_valid(self):
        form_data = {
            "username": "testusername",
            "first_name": "First name Test",
            "last_name": "Last name Test",
            "password1": "123testadmin!QW",
            "password2": "123testadmin!QW",
            "years_of_experience": 10
        }

        form = CookCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.clean_years_of_experience())
        self.assertEqual(
            form.clean_years_of_experience(),
            form_data["years_of_experience"]
        )

    def test_author_update_with_clean_license_number_is_valid(self):
        form_data = {
            "years_of_experience": 10
        }

        form = CookUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.clean_years_of_experience())
        self.assertEqual(
            form.clean_years_of_experience(),
            form_data["years_of_experience"]
        )

    def test_search_driver_is_valid(self):
        form_data = {
            "empty": {"title": ""},
            "not_empty": {"title": "test"}
        }

        form_empty = CookSearchForm(form_data["empty"])
        form_not_empty = CookSearchForm(form_data["not_empty"])

        self.assertTrue(form_empty.is_valid())
        self.assertTrue(form_not_empty.is_valid())
        self.assertEqual(
            form_empty.fields["title"].widget.attrs["placeholder"],
            "Search by username:"
        )

    def test_search_car_is_valid(self):
        form_data = {
            "empty": {"title": ""},
            "not_empty": {"title": "test"}
        }

        form_empty = DishSearchForm(form_data["empty"])
        form_not_empty = DishSearchForm(form_data["not_empty"])

        self.assertTrue(form_empty.is_valid())
        self.assertTrue(form_not_empty.is_valid())
        self.assertEqual(
            form_empty.fields["title"].widget.attrs["placeholder"],
            "Search by name:"
        )

    def test_search_manufacturer_form_is_valid(self):
        form_data = {
            "empty": {"title": ""},
            "not_empty": {"title": "test"}
        }

        form_empty = DishTypeSearchForm(form_data["empty"])
        form_not_empty = DishTypeSearchForm(form_data["not_empty"])

        self.assertTrue(form_empty.is_valid())
        self.assertTrue(form_not_empty.is_valid())
        self.assertEqual(
            form_empty.fields["title"].widget.attrs["placeholder"],
            "Search by name:"
        )
