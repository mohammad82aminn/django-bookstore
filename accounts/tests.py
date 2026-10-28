from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reader",
            password="Bookstore-Test-Password-42!",
        )

    def test_login_page(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "reader",
                "password": "Bookstore-Test-Password-42!",
            },
        )

        self.assertRedirects(response, reverse("pages:home"))

        home = self.client.get(reverse("pages:home"))

        self.assertTrue(home.context["user"].is_authenticated)
        self.assertEqual(home.context["user"].pk, self.user.pk)

    def test_login_with_wrong_password(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "reader",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertFalse(response.context["user"].is_authenticated)