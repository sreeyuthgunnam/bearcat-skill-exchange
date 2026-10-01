from django.shortcuts import redirect, render

from .forms import ListingSubmissionForm


def submit_listing(request):
    if request.method == 'POST':
        form = ListingSubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listings:submitted')
    else:
        form = ListingSubmissionForm()

    return render(request, 'listings/post.html', {'form': form})


def submission_received(request):
    return render(request, 'listings/submitted.html')