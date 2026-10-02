from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Listing


class ListingModelTests(TestCase):
    def listing_data(self, **overrides):
        data = {
            'display_name': 'Test Student',
            'offered_skill': Listing.OfferedSkill.CODING,
            'offer_description': 'I can help debug a small project.',
            'wanted_help': 'I would like help reviewing a résumé.',
            'contact_email': 'student@example.com',
        }
        data.update(overrides)
        return data

    def create_listing(self):
        return Listing.objects.create(**self.listing_data())

    def test_display_name_rejects_fewer_than_two_characters(self):
        listing = Listing(**self.listing_data(display_name='A'))

        with self.assertRaises(ValidationError) as error:
            listing.full_clean()

        self.assertIn('display_name', error.exception.message_dict)

    def test_offer_description_rejects_fewer_than_ten_characters(self):
        listing = Listing(**self.listing_data(offer_description='123456789'))

        with self.assertRaises(ValidationError) as error:
            listing.full_clean()

        self.assertIn('offer_description', error.exception.message_dict)

    def test_wanted_help_rejects_fewer_than_ten_characters(self):
        listing = Listing(**self.listing_data(wanted_help='123456789'))

        with self.assertRaises(ValidationError) as error:
            listing.full_clean()

        self.assertIn('wanted_help', error.exception.message_dict)

    def test_new_listing_is_pending_and_expires_after_fourteen_days(self):
        listing = self.create_listing()

        self.assertEqual(listing.status, Listing.Status.PENDING)
        self.assertEqual(listing.expires_at - listing.created_at, timedelta(days=14))

    def test_public_queryset_returns_only_approved_unexpired_listings(self):
        visible = self.create_listing()
        expired = self.create_listing()
        pending = self.create_listing()
        rejected = self.create_listing()
        closed = self.create_listing()

        Listing.objects.filter(pk=visible.pk).update(status=Listing.Status.APPROVED)
        Listing.objects.filter(pk=expired.pk).update(
            status=Listing.Status.APPROVED,
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        Listing.objects.filter(pk=rejected.pk).update(status=Listing.Status.REJECTED)
        Listing.objects.filter(pk=closed.pk).update(status=Listing.Status.CLOSED)

        public_ids = set(Listing.objects.public().values_list('pk', flat=True))

        self.assertSetEqual(public_ids, {visible.pk})
        self.assertNotIn(pending.pk, public_ids)


class ListingSubmissionTests(TestCase):
    def valid_submission(self):
        return {
            'display_name': 'Test Student',
            'offered_skill': Listing.OfferedSkill.CODING,
            'offer_description': 'I can help debug a small project.',
            'wanted_help': 'I would like help reviewing a résumé.',
            'availability': 'Weekday afternoons',
            'contact_email': 'student@example.com',
            'public_email_acknowledgment': 'on',
        }

    def test_root_redirects_to_submission_form(self):
        response = self.client.get('/')

        self.assertRedirects(response, reverse('listings:submit'))

    def test_get_displays_submission_form_and_public_email_acknowledgment(self):
        response = self.client.get(reverse('listings:submit'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'public_email_acknowledgment')
        self.assertContains(response, 'contact email will be public')

    def test_valid_submission_is_pending_and_redirects_to_confirmation(self):
        data = self.valid_submission()
        data.update({
            'status': Listing.Status.APPROVED,
            'created_at': '2000-01-01T00:00:00Z',
            'expires_at': '2000-01-02T00:00:00Z',
        })

        response = self.client.post(reverse('listings:submit'), data)

        self.assertRedirects(response, reverse('listings:submitted'))
        listing = Listing.objects.get()
        self.assertEqual(listing.status, Listing.Status.PENDING)
        self.assertNotEqual(listing.created_at.year, 2000)
        self.assertEqual(listing.expires_at - listing.created_at, timedelta(days=14))

        confirmation = self.client.get(response.url)
        self.assertContains(confirmation, 'Received for review')

    def test_invalid_submission_is_not_saved_and_displays_errors(self):
        data = self.valid_submission()
        data.update({
            'display_name': 'A',
            'offer_description': 'Too short',
            'wanted_help': 'Too short',
            'contact_email': 'not-an-email',
        })
        del data['public_email_acknowledgment']

        response = self.client.post(reverse('listings:submit'), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Listing.objects.count(), 0)
        self.assertSetEqual(
            set(response.context['form'].errors),
            {'display_name', 'offer_description', 'wanted_help', 'contact_email', 'public_email_acknowledgment'},
        )