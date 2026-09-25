from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra info attached to every User: are they an Organiser or a Cook?"""

    ROLE_CHOICES = [
        ("organiser", "Organiser"),
        ("cook", "Cook"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(
        max_length=30,
        blank=True,
        help_text="Optional — shown to the other side of a claim once a date is claimed.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Rota(models.Model):
    """A rota an Organiser sets up for someone who needs meals organised."""

    organiser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rotas",
    )
    recipient_name = models.CharField(max_length=100)
    occasion = models.CharField(max_length=150, blank=True)
    dietary_notes = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"Rota for {self.recipient_name} ({self.start_date} to {self.end_date})"


class Slot(models.Model):
    """A single cooking date within a Rota. Starts unclaimed; a Cook claims it."""

    rota = models.ForeignKey(Rota, on_delete=models.CASCADE, related_name="slots")
    date = models.DateField()
    cook = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="claimed_slots",
    )
    notes = models.TextField(blank=True)
    preferred_time = models.CharField(
        max_length=50,
        blank=True,
        help_text='Optional — e.g. "around 6pm" or "after school pickup".',
    )
    claimed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        cook_name = self.cook.username if self.cook else "unclaimed"
        return f"{self.rota.recipient_name} — {self.date} ({cook_name})"
