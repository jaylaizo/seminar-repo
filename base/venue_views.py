from django.contrib.auth.decorators import login_required, user_passes_test
# base/views/venue_views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from base.forms import VenueForm
from django.contrib.auth.decorators import login_required

@login_required
def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venue added successfully.')
            return redirect('add_venue')
    else:
        form = VenueForm()
    
    return render(request, 'venue_templates/add_venue.html', {'form': form})

