from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib import messages


def show_message(sender, user, request, **kwargs):
    messages.info(request, 'You have been logged out.')
    print('sending message')

def logged_in_message(sender, user, request, **kwargs):
    """
    Add a welcome message when the user logs in
    """
    messages.info(request, "Welcome ...")

user_logged_in.connect(logged_in_message)
user_logged_out.connect(show_message)