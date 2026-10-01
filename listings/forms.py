from django import forms

from .models import Listing


class ListingSubmissionForm(forms.ModelForm):
    public_email_acknowledgment = forms.BooleanField(
        label='I understand my contact email will be public if this listing is approved.',
        required=True,
    )

    class Meta:
        model = Listing
        fields = [
            'display_name',
            'offered_skill',
            'offer_description',
            'wanted_help',
            'availability',
            'contact_email',
        ]
        labels = {
            'offered_skill': 'Offered skill category',
            'offer_description': 'Specific offer',
            'wanted_help': 'Wanted help',
        }
        widgets = {
            'offer_description': forms.Textarea(attrs={'rows': 4}),
            'wanted_help': forms.Textarea(attrs={'rows': 4}),
            'availability': forms.Textarea(attrs={'rows': 3}),
        }
