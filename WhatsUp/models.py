from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Ticket(models.Model):
    NEW = 'N'
    IN_PROGRESS = 'IP'
    DONE = 'D'
    INVALID = 'IV'
    TICKET_STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'), 
        (DONE, 'Done'),
        (INVALID, 'Invalid')
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    ticket_status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES, default=NEW)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by+')
    assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_user+',
        default=None,
        null=True,
        blank=True)
    finished_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='finished_user+',
        default=None,
        null=True)

    def __str__(self):
        return self.title
