import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def _safe_send(subject, message, recipient):
    if not recipient:
        return
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        logger.info('Email sent to %s (%s)', recipient, subject)
    except Exception as e:
        logger.error('Could not send email to %s: %s', recipient, e)


def notify_ticket_created(ticket):
    subject = f'Ticket "{ticket.title}" has been registered'
    message = (
        f'Hello, {ticket.created_by.username}!\n\n'
        f'Your ticket "{ticket.title}" has been created.\n'
        f'Ticket number: {ticket.ticket_number}\n'
        f'Current status: {ticket.ticket_status}\n\n'
        f'A support engineer will pick it up soon.'
    )
    _safe_send(subject, message, ticket.created_by.email)


def notify_status_changed(ticket):
    subject = f'Ticket "{ticket.title}" status changed: {ticket.ticket_status}'
    message = (
        f'Hello, {ticket.created_by.username}!\n\n'
        f'The status of your ticket "{ticket.title}" '
        f'changed to "{ticket.ticket_status}".\n'
        f'Ticket number: {ticket.ticket_number}'
    )
    _safe_send(subject, message, ticket.created_by.email)
