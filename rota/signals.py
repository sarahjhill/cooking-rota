from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def announce_login(sender, request, user, **kwargs):
    """Show a welcome-back message every time anyone logs in.

    Guarded with hasattr(): Django's test client has a `self.client.login()`
    shortcut that signs a user in for test setup without running the request
    through MessageMiddleware, so `request._messages` won't exist there. This
    check keeps that shortcut working everywhere else in the test suite,
    while still showing the real message on every actual browser login.
    """
    if hasattr(request, "_messages"):
        messages.success(request, f"Welcome back, {user.username}.")


@receiver(user_logged_out)
def announce_logout(sender, request, user, **kwargs):
    """Show a confirmation message every time anyone logs out."""
    if hasattr(request, "_messages"):
        messages.success(request, "You've been logged out.")
