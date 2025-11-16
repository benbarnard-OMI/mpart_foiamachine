"""
AI Agent service layer - Core logic for agent operations
"""

import logging
from typing import Dict, Any, Optional
from django.conf import settings
from .models import AgentTask

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, user, model: str = None):
        self.user = user
        self.model = model or settings.AGENT_CONFIG.get('MODEL', 'gpt-4-turbo-preview')
        self.temperature = settings.AGENT_CONFIG.get('TEMPERATURE', 0.7)
        self.api_key = settings.AGENT_CONFIG.get('OPENAI_API_KEY')
    
    def create_task(self, task_type: str, input_data: Dict[str, Any], 
                    foia_request=None) -> AgentTask:
        """Create an agent task record"""
        return AgentTask.objects.create(
            task_type=task_type,
            user=self.user,
            foia_request=foia_request,
            input_data=input_data,
            agent_model=self.model,
            status='pending'
        )
    
    def _call_llm(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """
        Call the LLM API
        Returns: Dict with 'content' and 'tokens_used'
        """
        # This is a placeholder - actual implementation would call OpenAI API
        # For now, we'll return a mock response
        logger.info(f"LLM call with model {self.model}")
        
        # In production, this would use OpenAI's API:
        # from openai import OpenAI
        # client = OpenAI(api_key=self.api_key)
        # response = client.chat.completions.create(...)
        
        return {
            'content': f"[AI Generated Response - Production will use {self.model}]",
            'tokens_used': 100
        }


class RequestDraftAgent(BaseAgent):
    """Agent specialized in drafting FOIA requests"""
    
    def draft_request(self, description: str, agency_name: str, 
                     agency_type: str) -> Dict[str, Any]:
        """
        Draft a FOIA request based on user's description
        
        Args:
            description: User's description of what they want to request
            agency_name: Name of the target agency
            agency_type: Type of agency (federal, state, local)
        
        Returns:
            Dict containing drafted request text and metadata
        """
        task = self.create_task('draft_request', {
            'description': description,
            'agency_name': agency_name,
            'agency_type': agency_type
        })
        
        try:
            task.status = 'processing'
            task.save()
            
            system_prompt = """You are a FOIA request drafting expert. 
            Draft professional, legally sound FOIA requests that are:
            - Clear and specific
            - Properly formatted with legal language
            - Scope-appropriate to avoid overly broad rejections
            - Include proper fee waiver language if applicable"""
            
            prompt = f"""Draft a FOIA request for the following:
            
            Agency: {agency_name} ({agency_type})
            Request Description: {description}
            
            Include:
            1. Proper legal opening
            2. Clear description of requested records
            3. Reasonable time frame if applicable
            4. Fee waiver request if appropriate
            5. Contact information placeholders
            6. Professional closing
            
            Format the request as a complete, ready-to-send letter."""
            
            result = self._call_llm(prompt, system_prompt)
            
            output = {
                'request_text': result['content'],
                'suggestions': [
                    'Review the scope to ensure it\'s not too broad',
                    'Add specific date ranges if possible',
                    'Consider requesting electronic format'
                ]
            }
            
            task.output_data = output
            task.tokens_used = result['tokens_used']
            task.status = 'completed'
            task.save()
            
            return output
            
        except Exception as e:
            task.status = 'failed'
            task.error_message = str(e)
            task.save()
            logger.error(f"Request draft failed: {e}")
            raise


class ResponseAnalysisAgent(BaseAgent):
    """Agent specialized in analyzing agency responses"""
    
    def analyze_response(self, response_text: str, 
                        original_request: str) -> Dict[str, Any]:
        """
        Analyze an agency's response to a FOIA request
        
        Args:
            response_text: The agency's response text
            original_request: The original FOIA request text
        
        Returns:
            Dict containing analysis and recommendations
        """
        task = self.create_task('analyze_response', {
            'response_text': response_text,
            'original_request': original_request
        })
        
        try:
            task.status = 'processing'
            task.save()
            
            system_prompt = """You are a FOIA response analysis expert.
            Analyze agency responses for:
            - Level of compliance with the request
            - Exemptions claimed and their validity
            - Next steps or follow-up actions needed
            - Appeal opportunities"""
            
            prompt = f"""Analyze this FOIA response:
            
            Original Request: {original_request[:500]}...
            
            Agency Response: {response_text}
            
            Provide:
            1. Summary of what was provided
            2. What was denied or redacted (with exemptions cited)
            3. Assessment of response adequacy
            4. Recommended next steps (accept, follow-up, or appeal)
            5. Key dates or deadlines mentioned"""
            
            result = self._call_llm(prompt, system_prompt)
            
            output = {
                'summary': result['content'],
                'compliance_level': 'partial',  # Would be extracted from analysis
                'requires_followup': True,
                'recommended_action': 'follow_up',
                'key_points': []
            }
            
            task.output_data = output
            task.tokens_used = result['tokens_used']
            task.status = 'completed'
            task.save()
            
            return output
            
        except Exception as e:
            task.status = 'failed'
            task.error_message = str(e)
            task.save()
            logger.error(f"Response analysis failed: {e}")
            raise


class FollowUpAgent(BaseAgent):
    """Agent specialized in generating follow-up communications"""
    
    def generate_followup(self, request_context: Dict[str, Any],
                         followup_reason: str) -> Dict[str, Any]:
        """
        Generate a follow-up communication
        
        Args:
            request_context: Context about the original request
            followup_reason: Reason for follow-up (e.g., 'no_response', 'incomplete')
        
        Returns:
            Dict containing follow-up text and metadata
        """
        task = self.create_task('generate_followup', {
            'context': request_context,
            'reason': followup_reason
        })
        
        try:
            task.status = 'processing'
            task.save()
            
            system_prompt = """You are a FOIA follow-up communication expert.
            Generate professional follow-up messages that are:
            - Polite but firm
            - Reference relevant deadlines and laws
            - Clear about what action is needed
            - Professional in tone"""
            
            prompt = f"""Generate a follow-up communication for:
            
            Reason: {followup_reason}
            Original Request: {request_context.get('title', 'N/A')}
            Days Since Submission: {request_context.get('days_elapsed', 0)}
            
            Create a professional follow-up that addresses the situation."""
            
            result = self._call_llm(prompt, system_prompt)
            
            output = {
                'followup_text': result['content'],
                'suggested_subject': f"Follow-up: {request_context.get('title', 'FOIA Request')}",
                'urgency': 'medium'
            }
            
            task.output_data = output
            task.tokens_used = result['tokens_used']
            task.status = 'completed'
            task.save()
            
            return output
            
        except Exception as e:
            task.status = 'failed'
            task.error_message = str(e)
            task.save()
            logger.error(f"Follow-up generation failed: {e}")
            raise


class DocumentSummaryAgent(BaseAgent):
    """Agent specialized in summarizing documents"""
    
    def summarize_document(self, document_content: str,
                          document_type: str = 'response') -> Dict[str, Any]:
        """
        Summarize a document
        
        Args:
            document_content: The document text content
            document_type: Type of document (request, response, etc.)
        
        Returns:
            Dict containing summary and key points
        """
        task = self.create_task('summarize_document', {
            'document_type': document_type,
            'content_length': len(document_content)
        })
        
        try:
            task.status = 'processing'
            task.save()
            
            system_prompt = """You are a document summarization expert.
            Create concise, accurate summaries that capture:
            - Main points and key information
            - Important dates and deadlines
            - Actions required
            - Critical details"""
            
            prompt = f"""Summarize this {document_type} document:
            
            {document_content[:2000]}...
            
            Provide:
            1. Brief overview (2-3 sentences)
            2. Key points (bullet list)
            3. Important dates or deadlines
            4. Action items"""
            
            result = self._call_llm(prompt, system_prompt)
            
            output = {
                'summary': result['content'],
                'key_points': [],
                'word_count': len(document_content.split())
            }
            
            task.output_data = output
            task.tokens_used = result['tokens_used']
            task.status = 'completed'
            task.save()
            
            return output
            
        except Exception as e:
            task.status = 'failed'
            task.error_message = str(e)
            task.save()
            logger.error(f"Document summarization failed: {e}")
            raise
