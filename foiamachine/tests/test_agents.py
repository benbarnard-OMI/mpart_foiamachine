"""
Tests for the Agent services
"""

import pytest
from django.contrib.auth import get_user_model
from foiamachine.apps.agents.services import (
    RequestDraftAgent,
    ResponseAnalysisAgent,
    FollowUpAgent,
    DocumentSummaryAgent
)
from foiamachine.apps.agents.models import AgentTask

User = get_user_model()


@pytest.mark.django_db
class TestRequestDraftAgent:
    """Tests for the Request Drafting Agent"""
    
    def test_draft_request_creates_task(self):
        """Test that drafting a request creates an agent task"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        agent = RequestDraftAgent(user)
        
        result = agent.draft_request(
            description="I need records about...",
            agency_name="Test Agency",
            agency_type="federal"
        )
        
        assert 'request_text' in result
        assert 'suggestions' in result
        
        # Check that a task was created
        task = AgentTask.objects.filter(user=user, task_type='draft_request').first()
        assert task is not None
        assert task.status == 'completed'
    
    def test_draft_request_with_empty_description(self):
        """Test that drafting fails with empty description"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        agent = RequestDraftAgent(user)
        
        # This should still work but produce generic output
        result = agent.draft_request(
            description="",
            agency_name="Test Agency",
            agency_type="federal"
        )
        
        assert 'request_text' in result


@pytest.mark.django_db
class TestResponseAnalysisAgent:
    """Tests for the Response Analysis Agent"""
    
    def test_analyze_response_creates_task(self):
        """Test that analyzing a response creates a task"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        agent = ResponseAnalysisAgent(user)
        
        result = agent.analyze_response(
            response_text="The agency responded with...",
            original_request="I requested..."
        )
        
        assert 'summary' in result
        assert 'compliance_level' in result
        assert 'requires_followup' in result
        
        # Check that a task was created
        task = AgentTask.objects.filter(user=user, task_type='analyze_response').first()
        assert task is not None


@pytest.mark.django_db
class TestFollowUpAgent:
    """Tests for the Follow-up Agent"""
    
    def test_generate_followup(self):
        """Test follow-up generation"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        agent = FollowUpAgent(user)
        
        context = {
            'title': 'Test Request',
            'agency': 'Test Agency',
            'days_elapsed': 30
        }
        
        result = agent.generate_followup(context, 'no_response')
        
        assert 'followup_text' in result
        assert 'suggested_subject' in result
        
        # Check that a task was created
        task = AgentTask.objects.filter(user=user, task_type='generate_followup').first()
        assert task is not None


@pytest.mark.django_db
class TestDocumentSummaryAgent:
    """Tests for the Document Summary Agent"""
    
    def test_summarize_document(self):
        """Test document summarization"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        agent = DocumentSummaryAgent(user)
        
        document_content = "This is a long document with lots of content... " * 100
        
        result = agent.summarize_document(document_content, 'response')
        
        assert 'summary' in result
        assert 'key_points' in result
        assert 'word_count' in result
        
        # Check that a task was created
        task = AgentTask.objects.filter(user=user, task_type='summarize_document').first()
        assert task is not None
