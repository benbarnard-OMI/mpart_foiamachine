"""
Agency views
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Agency


@login_required
def agency_list(request):
    """List all active agencies"""
    agencies = Agency.objects.filter(is_active=True, is_deleted=False)
    return render(request, 'agency/agency_list.html', {
        'agencies': agencies
    })


@login_required
def agency_detail(request, slug):
    """Display agency details"""
    agency = get_object_or_404(Agency, slug=slug, is_deleted=False)
    return render(request, 'agency/agency_detail.html', {
        'agency': agency
    })
