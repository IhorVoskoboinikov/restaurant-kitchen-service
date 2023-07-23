from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Dish


class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "testusername"
        cls.password = "123testadmin"
        cls.years_of_experience = 10

        cls.dish_type = DishType.objects.create(
            name="cook-type-test",
        )
        cls.cook = get_user_model().objects.create_user(
            username="testusername",
            first_name="First name Test",
            last_name="Last name Test",
            password="123testadmin",
            years_of_experience=10
        )

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_cook_str(self):
        str_name = (f"{self.cook.username} "
                    f"({self.cook.first_name} {self.cook.last_name})")
        self.assertEqual(str(self.cook), str_name)

    def test_dish_str(self):
        dish = Dish.objects.create(
            name="Bread",
            dish_type=self.dish_type,
            description="Test description",
            price="1.25",
        )
        dish.cooks.add(self.cook)
        expected_name = f"{dish.name} ({dish.price})"

        self.assertEqual(str(dish), expected_name)

    def test_create_cook_years_of_experience(self):
        self.assertEqual(self.cook.username, self.username)
        self.assertTrue(self.cook.check_password(self.password))
        self.assertEqual(
            self.cook.years_of_experience,
            self.years_of_experience
        )

    def test_get_driver_absolute_url(self):
        self.assertEqual(
            self.cook.get_absolute_url(),
            "/cooks/1/"
        )
