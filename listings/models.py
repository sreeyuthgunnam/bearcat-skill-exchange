from datetime import timedelta
import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


class ListingQuerySet(models.QuerySet):
    def public(self):
        return self.filter(
            status=Listing.Status.APPROVED,
            expires_at__gt=timezone.now(),
        )


class Listing(models.Model):
    class OfferedSkill(models.TextChoices):
        DESIGN = 'design', 'Design'
        PHOTOGRAPHY = 'photography', 'Photography'
        CODING = 'coding', 'Coding'
        WRITING = 'writing', 'Writing'
        PRESENTATIONS = 'presentations', 'Presentations'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CLOSED = 'closed', 'Closed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=60, validators=[MinLengthValidator(2)])
    offered_skill = models.CharField(max_length=32, choices=OfferedSkill.choices)
    offer_description = models.CharField(max_length=500, validators=[MinLengthValidator(10)])
    wanted_help = models.CharField(max_length=500, validators=[MinLengthValidator(10)])
    availability = models.CharField(max_length=200, blank=True, default='')
    contact_email = models.EmailField(max_length=254)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(editable=False)
    expires_at = models.DateTimeField(editable=False)

    objects = ListingQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(
                fields=['status', 'offered_skill', 'created_at'],
                name='listing_status_skill_created',
            ),
        ]
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.status = self.Status.PENDING
            self.created_at = timezone.now()
            self.expires_at = self.created_at + timedelta(days=14)
        super().save(*args, **kwargs)