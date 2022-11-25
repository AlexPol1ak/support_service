from django.core.mail import send_mail

from support.settings import EMAIL_HOST_USER


def send_email_user(*, user_email :str, user_title :str, support_message :str, support_name :str) ->str:
    """Sends an email with a response to the ticket to the user."""
    try:
        send_mail(
            f"There was a response '{user_title}....' to your appeal.",
            f"{support_message}.\n Support service, {support_name}.",
            recipient_list=[user_email],
            from_email=EMAIL_HOST_USER,
            fail_silently =False,
        )
    except Exception as e:
        return str(e)

    return "A message has been sent."