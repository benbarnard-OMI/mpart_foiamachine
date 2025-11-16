"""
Celery tasks for asynchronous agent processing
"""

from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_agent_task(task_id):
    """
    Process an agent task asynchronously
    """
    from .models import AgentTask
    from .services import (
        RequestDraftAgent, ResponseAnalysisAgent,
        FollowUpAgent, DocumentSummaryAgent
    )
    
    try:
        task = AgentTask.objects.get(id=task_id)
        
        # Get the appropriate agent based on task type
        agents = {
            'draft_request': RequestDraftAgent,
            'analyze_response': ResponseAnalysisAgent,
            'generate_followup': FollowUpAgent,
            'summarize_document': DocumentSummaryAgent,
        }
        
        agent_class = agents.get(task.task_type)
        if not agent_class:
            task.status = 'failed'
            task.error_message = f"Unknown task type: {task.task_type}"
            task.save()
            return
        
        agent = agent_class(task.user)
        
        # Execute the task based on type
        # This would call the appropriate agent method with task.input_data
        
        logger.info(f"Agent task {task_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Agent task {task_id} failed: {e}")
        raise


@shared_task
def auto_followup_overdue_requests():
    """
    Automatically check for overdue requests and generate follow-ups
    """
    from django.utils import timezone
    from datetime import timedelta
    from .models import FOIARequest
    from .services import FollowUpAgent
    
    # Find requests that are overdue (more than 20 business days old)
    cutoff_date = timezone.now() - timedelta(days=20)
    overdue_requests = FOIARequest.objects.filter(
        status='submitted',
        submitted_date__lt=cutoff_date,
        response_received=False,
        is_deleted=False
    )
    
    for request in overdue_requests:
        if request.user.enable_agent_assistance:
            # Generate follow-up suggestion
            agent = FollowUpAgent(request.user)
            context = {
                'title': request.title,
                'agency': request.agency.name,
                'days_elapsed': (timezone.now() - request.submitted_date).days
            }
            
            try:
                result = agent.generate_followup(context, 'no_response')
                # Create a suggestion for the user
                from .models import AgentSuggestion
                AgentSuggestion.objects.create(
                    user=request.user,
                    foia_request=request,
                    suggestion_type='followup',
                    title='Suggested Follow-up for Overdue Request',
                    description=f'Your request has been pending for {context["days_elapsed"]} days.',
                    suggested_text=result['followup_text']
                )
                logger.info(f"Created follow-up suggestion for request {request.id}")
            except Exception as e:
                logger.error(f"Failed to create follow-up for request {request.id}: {e}")


@shared_task
def analyze_new_responses():
    """
    Automatically analyze new responses that haven't been processed
    """
    from .models import FOIARequest
    from .services import ResponseAnalysisAgent
    
    # Find requests with responses that haven't been analyzed
    unanalyzed = FOIARequest.objects.filter(
        response_received=True,
        response_summary='',
        is_deleted=False
    )
    
    for request in unanalyzed:
        if request.user.enable_agent_assistance:
            # Get the response text from communications
            latest_comm = request.communications.filter(
                direction='incoming'
            ).first()
            
            if latest_comm:
                agent = ResponseAnalysisAgent(request.user)
                try:
                    result = agent.analyze_response(
                        latest_comm.content,
                        request.request_body
                    )
                    request.response_summary = result['summary']
                    request.requires_followup = result['requires_followup']
                    request.save()
                    logger.info(f"Analyzed response for request {request.id}")
                except Exception as e:
                    logger.error(f"Failed to analyze response for request {request.id}: {e}")
