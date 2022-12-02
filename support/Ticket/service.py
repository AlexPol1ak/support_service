from django.core.mail import send_mail
from django.utils import timezone

from support.settings import EMAIL_HOST_USER


def send_email_user(user_email: str, user_title :str, support_name :str, support_message :str,
                    frozen = None, resolved = None) -> str:
    """Sends an email with a response to the ticket to the user."""

    title = f"There was a response '{user_title}...' to your appeal."
    text = '\n'+ support_message
    signature =f"\nSupport service, {support_name}.\n"

    message = ''
    if support_message:
        message += text
    if frozen:
        message += '\nYour appeal is temporarily frozen.'
    if resolved:
        message += '\nYour appeal is closed.'

    message += signature
    message += timezone.now().strftime('%d-%m-%Y %H:%M')

    try:
        send_mail(
            title,
            message,
            recipient_list=[user_email],
            from_email=EMAIL_HOST_USER,
            fail_silently =False,
        )
    except Exception as e:
        return str(e)

    return "A message has been sent."