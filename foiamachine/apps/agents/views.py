"""
Agent views - User-facing interfaces for agent features
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .services import RequestDraftAgent, ResponseAnalysisAgent, FollowUpAgent
from .models import AgentTask, AgentSuggestion
from foiamachine.apps.requests.models import FOIARequest


@login_required
def agent_dashboard(request):
    """Agent dashboard showing recent tasks and suggestions"""
    recent_tasks = AgentTask.objects.filter(user=request.user)[:10]
    pending_suggestions = AgentSuggestion.objects.filter(
        user=request.user,
        is_accepted=False,
        is_rejected=False
    )
    
    return render(request, 'agents/dashboard.html', {
        'recent_tasks': recent_tasks,
        'pending_suggestions': pending_suggestions,
    })


@login_required
@require_http_methods(["POST"])
def draft_request_with_agent(request):
    """API endpoint to draft a FOIA request using AI agent"""
    try:
        data = json.loads(request.body)
        description = data.get('description')
        agency_name = data.get('agency_name')
        agency_type = data.get('agency_type', 'federal')
        
        if not description or not agency_name:
            return JsonResponse({
                'error': 'Description and agency name are required'
            }, status=400)
        
        # Use the agent to draft the request
        agent = RequestDraftAgent(request.user)
        result = agent.draft_request(description, agency_name, agency_type)
        
        return JsonResponse({
            'success': True,
            'request_text': result['request_text'],
            'suggestions': result['suggestions']
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def analyze_response_with_agent(request, request_id):
    """API endpoint to analyze a response using AI agent"""
    try:
        foia_request = get_object_or_404(
            FOIARequest,
            id=request_id,
            user=request.user
        )
        
        data = json.loads(request.body)
        response_text = data.get('response_text')
        
        if not response_text:
            return JsonResponse({
                'error': 'Response text is required'
            }, status=400)
        
        # Use the agent to analyze the response
        agent = ResponseAnalysisAgent(request.user)
        result = agent.analyze_response(
            response_text,
            foia_request.request_body
        )
        
        # Update the request with analysis
        foia_request.response_summary = result['summary']
        foia_request.requires_followup = result['requires_followup']
        foia_request.save()
        
        return JsonResponse({
            'success': True,
            'analysis': result
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def generate_followup_with_agent(request, request_id):
    """API endpoint to generate a follow-up using AI agent"""
    try:
        foia_request = get_object_or_404(
            FOIARequest,
            id=request_id,
            user=request.user
        )
        
        data = json.loads(request.body)
        reason = data.get('reason', 'no_response')
        
        # Prepare context
        context = {
            'title': foia_request.title,
            'agency': foia_request.agency.name,
            'submitted_date': str(foia_request.submitted_date) if foia_request.submitted_date else None,
            'tracking_number': foia_request.tracking_number,
        }
        
        # Use the agent to generate follow-up
        agent = FollowUpAgent(request.user)
        result = agent.generate_followup(context, reason)
        
        return JsonResponse({
            'success': True,
            'followup': result
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


@login_required
def task_detail(request, task_id):
    """View details of an agent task"""
    task = get_object_or_404(AgentTask, id=task_id, user=request.user)
    
    return render(request, 'agents/task_detail.html', {
        'task': task
    })


@login_required
@require_http_methods(["POST"])
def accept_suggestion(request, suggestion_id):
    """Accept an agent suggestion"""
    suggestion = get_object_or_404(
        AgentSuggestion,
        id=suggestion_id,
        user=request.user
    )
    
    suggestion.is_accepted = True
    suggestion.save()
    
    messages.success(request, 'Suggestion accepted!')
    return redirect('agents:dashboard')


@login_required
@require_http_methods(["POST"])
def reject_suggestion(request, suggestion_id):
    """Reject an agent suggestion"""
    suggestion = get_object_or_404(
        AgentSuggestion,
        id=suggestion_id,
        user=request.user
    )
    
    data = json.loads(request.body) if request.body else {}
    suggestion.is_rejected = True
    suggestion.feedback = data.get('feedback', '')
    suggestion.save()
    
    return JsonResponse({'success': True})
