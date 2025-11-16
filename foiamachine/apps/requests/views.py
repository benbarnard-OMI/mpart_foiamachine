"""
FOIA Request views
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FOIARequest


@login_required
def request_list(request):
    """List all requests for the current user"""
    requests = FOIARequest.objects.filter(
        user=request.user,
        is_deleted=False
    )
    return render(request, 'requests/request_list.html', {
        'requests': requests
    })


@login_required
def request_detail(request, pk):
    """Display request details"""
    foia_request = get_object_or_404(
        FOIARequest,
        pk=pk,
        user=request.user,
        is_deleted=False
    )
    return render(request, 'requests/request_detail.html', {
        'request': foia_request,
        'communications': foia_request.communications.all(),
        'documents': foia_request.documents.all(),
    })


@login_required
def request_create(request):
    """Create a new FOIA request"""
    if request.method == 'POST':
        # Form handling will be implemented with forms
        messages.success(request, 'Request created successfully!')
        return redirect('requests:list')
    
    return render(request, 'requests/request_form.html', {
        'title': 'Create FOIA Request'
    })
