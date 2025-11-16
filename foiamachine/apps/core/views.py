"""
Core views for the main application
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Homepage view"""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = 'MPART FOIA Machine'
        return context


@login_required
def dashboard(request):
    """User dashboard view"""
    return render(request, 'core/dashboard.html', {
        'user': request.user,
    })
