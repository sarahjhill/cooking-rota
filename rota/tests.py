from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile, Rota, Slot


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

        self.other_organiser = User.objects.create_user(
            username="org2", password="Sturdy-Passphrase-42"
        )
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
        start = date.today() + timedelta(days=30)
        end = start + timedelta(days=13)
        response = self.client.post(reverse("rota:rota_create"), {
            "recipient_name": "Priya",
            "occasion": "",
            "dietary_notes": "",
            "address": "",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
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


class SlotCRUDTests(TestCase):

    def setUp(self):
        self.organiser = User.objects.create_user(username="org1", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.organiser, role="organiser")

        self.cook = User.objects.create_user(username="cook1", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.cook, role="cook")

        self.other_cook = User.objects.create_user(
            username="cook2", password="Sturdy-Passphrase-42"
        )
        Profile.objects.create(user=self.other_cook, role="cook")

        self.rota = Rota.objects.create(
            organiser=self.organiser,
            recipient_name="Jo",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 14),
        )
        self.slot = Slot.objects.create(rota=self.rota, date=date(2026, 1, 3))

    def test_organiser_can_add_a_slot(self):
        self.client.login(username="org1", password="Sturdy-Passphrase-42")
        new_slot_date = date.today() + timedelta(days=5)
        response = self.client.post(reverse("rota:slot_create", args=[self.rota.pk]), {
            "date": new_slot_date.isoformat(),
            "notes": "",
        })
        self.assertEqual(self.rota.slots.count(), 2)
        self.assertRedirects(response, reverse("rota:rota_detail", args=[self.rota.pk]))

    def test_cook_cannot_add_a_slot(self):
        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:slot_create", args=[self.rota.pk]))
        self.assertEqual(response.status_code, 403)

    def test_cook_can_claim_an_open_slot(self):
        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:slot_claim", args=[self.slot.pk]))
        self.assertRedirects(response, reverse("rota:rota_detail", args=[self.rota.pk]))

        self.slot.refresh_from_db()
        self.assertEqual(self.slot.cook, self.cook)
        self.assertIsNotNone(self.slot.claimed_at)

    def test_cook_cannot_claim_an_already_claimed_slot(self):
        self.slot.cook = self.cook
        self.slot.save()

        self.client.login(username="cook2", password="Sturdy-Passphrase-42")
        self.client.post(reverse("rota:slot_claim", args=[self.slot.pk]))

        self.slot.refresh_from_db()
        self.assertEqual(self.slot.cook, self.cook)

    def test_cook_can_cancel_their_own_claim(self):
        self.slot.cook = self.cook
        self.slot.save()

        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        self.client.post(reverse("rota:slot_cancel", args=[self.slot.pk]))

        self.slot.refresh_from_db()
        self.assertIsNone(self.slot.cook)

    def test_cook_cannot_cancel_someone_elses_claim(self):
        self.slot.cook = self.cook
        self.slot.save()

        self.client.login(username="cook2", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:slot_cancel", args=[self.slot.pk]))
        self.assertEqual(response.status_code, 403)

        self.slot.refresh_from_db()
        self.assertEqual(self.slot.cook, self.cook)


class OwnershipPermissionTests(TestCase):
    def setUp(self):
        self.organiser = User.objects.create_user(username="org1", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.organiser, role="organiser")

        self.other_organiser = User.objects.create_user(
            username="org2", password="Sturdy-Passphrase-42"
        )
        Profile.objects.create(user=self.other_organiser, role="organiser")

        self.cook = User.objects.create_user(username="cook1", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.cook, role="cook")

        self.rota = Rota.objects.create(
            organiser=self.organiser,
            recipient_name="Jo",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 14),
        )
        self.slot = Slot.objects.create(rota=self.rota, date=date(2026, 1, 3))

    def test_anonymous_visitor_redirected_to_login_not_500(self):
        response = self.client.get(reverse("rota:rota_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_other_organiser_cannot_delete_this_rota(self):
        self.client.login(username="org2", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:rota_delete", args=[self.rota.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Rota.objects.filter(pk=self.rota.pk).exists())

    def test_other_organiser_cannot_add_a_slot_to_this_rota(self):
        self.client.login(username="org2", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:slot_create", args=[self.rota.pk]))
        self.assertEqual(response.status_code, 403)

    def test_other_organiser_cannot_edit_a_slot_on_this_rota(self):
        self.client.login(username="org2", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:slot_update", args=[self.slot.pk]))
        self.assertEqual(response.status_code, 403)

    def test_other_organiser_cannot_delete_a_slot_on_this_rota(self):
        self.client.login(username="org2", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:slot_delete", args=[self.slot.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Slot.objects.filter(pk=self.slot.pk).exists())

    def test_denied_attempt_returns_403_with_a_message_not_a_crash(self):
        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_create"))
        self.assertEqual(response.status_code, 403)


class NotificationTests(TestCase):
    """Every create/update/delete/claim/cancel action shows an on-page message."""

    def setUp(self):
        self.organiser = User.objects.create_user(
            username="organiser1", password="Sturdy-Passphrase-42"
        )
        Profile.objects.create(user=self.organiser, role="organiser")
        self.cook = User.objects.create_user(username="cook1", password="Sturdy-Passphrase-42")
        Profile.objects.create(user=self.cook, role="cook")
        self.rota = Rota.objects.create(
            organiser=self.organiser,
            recipient_name="Test Recipient",
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 14),
        )
        self.slot = Slot.objects.create(rota=self.rota, date=date(2026, 10, 5))

    def test_login_shows_welcome_back_message(self):
        response = self.client.post(
            reverse("login"),
            {"username": "organiser1", "password": "Sturdy-Passphrase-42"},
            follow=True,
        )
        self.assertContains(response, "Welcome back, organiser1.")

    def test_logout_shows_logged_out_message(self):
        self.client.login(username="organiser1", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("logout"), follow=True)
        self.assertContains(response, "You&#x27;ve been logged out.")

    def test_creating_a_rota_shows_a_message(self):
        self.client.login(username="organiser1", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:rota_create"), {
            "recipient_name": "New Recipient",
            "start_date": "2026-11-01",
            "end_date": "2026-11-14",
        }, follow=True)
        self.assertContains(response, "created.")

    def test_claiming_a_slot_shows_a_message(self):
        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        response = self.client.post(
            reverse("rota:slot_claim", args=[self.slot.pk]), follow=True
        )
        self.assertContains(response, "You&#x27;re down for")

    def test_cancelling_a_claim_shows_a_message(self):
        self.slot.cook = self.cook
        self.slot.save()
        self.client.login(username="cook1", password="Sturdy-Passphrase-42")
        response = self.client.post(
            reverse("rota:slot_cancel", args=[self.slot.pk]), follow=True
        )
        self.assertContains(response, "Date released")


class FormValidationTests(TestCase):
    """Forms reject bad input with a clear message, not a 500 or a silent save."""

    def setUp(self):
        self.organiser = User.objects.create_user(
            username="organiser3", password="Sturdy-Passphrase-42"
        )
        Profile.objects.create(user=self.organiser, role="organiser")
        self.rota = Rota.objects.create(
            organiser=self.organiser,
            recipient_name="Test Recipient",
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 14),
        )

    def test_rota_end_date_before_start_date_is_rejected(self):
        self.client.login(username="organiser3", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:rota_create"), {
            "recipient_name": "Backwards Rota",
            "start_date": "2026-11-14",
            "end_date": "2026-11-01",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "<li>The end date can't be before the start date.</li>",
            html=True,
        )
        self.assertFalse(Rota.objects.filter(recipient_name="Backwards Rota").exists())

    def test_slot_date_in_the_past_is_rejected(self):
        self.client.login(username="organiser3", password="Sturdy-Passphrase-42")
        yesterday = date.today() - timedelta(days=1)
        response = self.client.post(
            reverse("rota:slot_create", args=[self.rota.pk]),
            {"date": yesterday.isoformat(), "notes": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already passed")
        self.assertFalse(Slot.objects.filter(rota=self.rota, date=yesterday).exists())

    def test_valid_rota_is_still_accepted(self):
        self.client.login(username="organiser3", password="Sturdy-Passphrase-42")
        response = self.client.post(reverse("rota:rota_create"), {
            "recipient_name": "Valid Rota",
            "start_date": "2026-11-01",
            "end_date": "2026-11-14",
        }, follow=True)
        self.assertContains(response, "created.")
        self.assertTrue(Rota.objects.filter(recipient_name="Valid Rota").exists())


class PeerReviewFeedbackTests(TestCase):
    """Covers the two issues logged from the SME code review (#11, #12)."""

    def setUp(self):
        self.organiser = User.objects.create_user(
            username="organiser5",
            password="Sturdy-Passphrase-42",
            email="organiser5@example.com",
        )
        Profile.objects.create(user=self.organiser, role="organiser", phone="01234 567890")

        self.cook = User.objects.create_user(
            username="cook5",
            password="Sturdy-Passphrase-42",
            email="cook5@example.com",
        )
        Profile.objects.create(user=self.cook, role="cook", phone="07000 111222")

        self.other_cook = User.objects.create_user(
            username="cook6", password="Sturdy-Passphrase-42"
        )
        Profile.objects.create(user=self.other_cook, role="cook")

        self.rota = Rota.objects.create(
            organiser=self.organiser,
            recipient_name="Jo",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 14),
        )
        self.slot = Slot.objects.create(rota=self.rota, date=date(2026, 1, 3))

    def test_organiser_can_set_a_preferred_time_on_a_slot(self):
        """Issue #12 — claimed slots showed a date but no time."""
        self.client.login(username="organiser5", password="Sturdy-Passphrase-42")
        new_slot_date = date.today() + timedelta(days=5)
        self.client.post(reverse("rota:slot_create", args=[self.rota.pk]), {
            "date": new_slot_date.isoformat(),
            "preferred_time": "around 6pm",
            "notes": "",
        })

        new_slot = self.rota.slots.get(date=new_slot_date)
        self.assertEqual(new_slot.preferred_time, "around 6pm")

        response = self.client.get(reverse("rota:rota_detail", args=[self.rota.pk]))
        self.assertContains(response, "around 6pm")

    def test_cook_sees_organisers_contact_once_they_claim_a_slot(self):
        """Issue #11 — no way to contact the cook or organiser from a rota page."""
        self.slot.cook = self.cook
        self.slot.save()

        self.client.login(username="cook5", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_detail", args=[self.rota.pk]))

        self.assertContains(response, "organiser5@example.com")
        self.assertContains(response, "01234 567890")

    def test_organiser_sees_cooks_contact_once_a_slot_is_claimed(self):
        self.slot.cook = self.cook
        self.slot.save()

        self.client.login(username="organiser5", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_detail", args=[self.rota.pk]))

        self.assertContains(response, "cook5@example.com")
        self.assertContains(response, "07000 111222")

    def test_contact_details_not_shown_for_an_unclaimed_slot(self):
        self.client.login(username="organiser5", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_detail", args=[self.rota.pk]))
        self.assertNotContains(response, "07000 111222")

    def test_contact_details_not_shown_to_an_unrelated_cook(self):
        self.slot.cook = self.cook
        self.slot.save()

        self.client.login(username="cook6", password="Sturdy-Passphrase-42")
        response = self.client.get(reverse("rota:rota_detail", args=[self.rota.pk]))

        self.assertNotContains(response, "organiser5@example.com")
        self.assertNotContains(response, "cook5@example.com")
