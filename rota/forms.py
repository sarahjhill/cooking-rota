from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Profile, Rota, Slot


class SignUpForm(UserCreationForm):
    """Django's normal signup form, plus the Organiser/Cook choice."""

    email = forms.EmailField(
        required=True,
        help_text="We use this to send you rota updates.",
    )
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label="I am signing up as",
    )
    phone = forms.CharField(
        required=False,
        max_length=30,
        label="Phone (optional)",
        help_text="Only shown to the other side of a claim once a date is claimed — never shown publicly.",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # Show the fields in a sensible order rather than Django's default.
    field_order = ["username", "email", "role", "phone", "password1", "password2"]


class RotaForm(forms.ModelForm):
    """The fields an Organiser fills in to create or edit a rota."""

    class Meta:
        model = Rota
        fields = [
            "recipient_name",
            "occasion",
            "dietary_notes",
            "address",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "dietary_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_start_date(self):
        """No point creating a brand new rota that starts in the past.

        Only checked when creating a rota — an organiser editing an
        already-running rota shouldn't be blocked by its original start date.
        """
        start_date = self.cleaned_data.get("start_date")

        if start_date and not self.instance.pk and start_date < timezone.localdate():
            raise ValidationError("The start date can't be in the past.")

        return start_date

    def clean(self):
        """A rota that ends before it starts isn't something the model can catch on its own."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                "The end date can't be before the start date."
            )

        return cleaned_data


class SlotForm(forms.ModelForm):
    """The fields used to create or edit a single cooking slot."""

    class Meta:
        model = Slot
        fields = ["date", "preferred_time", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TextInput(attrs={"placeholder": "e.g. around 6pm"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def clean_date(self):
        """No point offering a cooking date that's already gone."""
        date = self.cleaned_data.get("date")

        if date and date < timezone.localdate():
            raise ValidationError("This date has already passed — pick a date from today onwards.")

        return date
