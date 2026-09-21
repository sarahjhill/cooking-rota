from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile, Rota


class SignUpTests(TestCase):
    """Registering creates a User, a Profile with the chosen role, and signs them in."""

    def test_signup_page_loads(self):
        response = self.client.get(reverse("rota:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_creates_user_and_profile(self):
        response = self.client.post(reverse("rota:signup"), {
            "username": "newcook",
            "email": "cook@example.com",
            "role": "cook",
            "password1": "Sturdy-Passphrase-42",
            "password2": "Sturdy-Passphrase-42",
        })

        self.assertRedirects(response, reverse("rota:home"))

        user = User.objects.get(username="newcook")
        self.assertEqual(user.profile.role, "cook")

    def test_mismatched_passwords_create_nothing(self):
        self.client.post(reverse("rota:signup"), {
            "username": "nope",
            "email": "nope@example.com",
            "role": "organiser",
            "password1": "Sturdy-Passphrase-42",
            "password2": "Different-Passphrase-43",
        })

        self.assertFalse(User.objects.filter(username="nope").exists())
        self.assertEqual(Profile.objects.count(), 0)


class LoginLogoutTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="organiser1",
            password="Sturdy-Passphrase-42",
        )
        Profile.objects.create(user=self.user, role="organiser")

    def test_login_works(self):
        logged_in = self.client.login(
            username="organiser1",
            password="Sturdy-Passphrase-42",
        )
        self.assertTrue(logged_in)

    def test_logout_requires_post(self):
        """Django 5 refuses a GET to the logout view."""
        self.client.login(username="organiser1", password="Sturdy-Passphrase-42")

        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertEqual(self.client.post(reverse("logout")).status_code, 302)


class RotaCRUDTests(TestCase):

    def setUp(self):
        self.organiser = User.objects.create_user(username="org1", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.organiser, role="organiser")

        self.other_organiser = User.objects.create_user(username="org2", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.other_organiser, role="organiser")

        self.cook = User.objects.create_user(username="cook1", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.cook, role="cook")

        self.rota = Rota.objects.create(
            organiser=self.organiser,
            recipient_name="Jo",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 14),
        )

    def test_cook_cannot_create_a_rota(self):
        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_create"))
        self.assertEqual(response.status_code, 403)

    def test_organiser_can_create_a_rota(self):
        self.client.login(username="org1", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:rota_create"), {
            "recipient_name": "Priya",
            "occasion": "",
            "dietary_notes": "",
            "address": "",
            "start_date": "2026-02-01",
            "end_date": "2026-02-14",
        })
        self.assertEqual(Rota.objects.filter(recipient_name="Priya").count(), 1)
        new_rota = Rota.objects.get(recipient_name="Priya")
        self.assertEqual(new_rota.organiser, self.organiser)
        self.assertRedirects(response, reverse("rota:rota_detail", args=[new_rota.pk]))

    def test_other_organiser_cannot_edit_this_rota(self):
        self.client.login(username="org2", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_update", args=[self.rota.pk]))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_their_rota(self):
        self.client.login(username="org1", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:rota_delete", args=[self.rota.pk]))
        self.assertRedirects(response, reverse("rota:home"))
        self.assertFalse(Rota.objects.filter(pk=self.rota.pk).exists())

    def test_anyone_signed_in_can_view_a_rota(self):
        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_detail", args=[self.rota.pk]))
        self.assertEqual(response.status_code, 200)
