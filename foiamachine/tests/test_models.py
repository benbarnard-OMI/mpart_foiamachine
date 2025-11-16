"""
Tests for the FOIA Request models
"""

import pytest
from django.contrib.auth import get_user_model
from foiamachine.apps.agency.models import Agency
from foiamachine.apps.requests.models import FOIARequest, RequestCommunication

User = get_user_model()


@pytest.mark.django_db
class TestFOIARequest:
    """Tests for the FOIA Request model"""
    
    def test_create_foia_request(self):
        """Test creating a FOIA request"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        agency = Agency.objects.create(
            name='Test Agency',
            slug='test-agency',
            level='federal'
        )
        
        request = FOIARequest.objects.create(
            title='Test Request',
            description='This is a test request',
            user=user,
            agency=agency,
            request_body='I am requesting...',
            status='draft'
        )
        
        assert request.title == 'Test Request'
        assert request.user == user
        assert request.agency == agency
        assert request.status == 'draft'
        assert not request.agent_assisted
    
    def test_foia_request_with_agent_assistance(self):
        """Test creating a FOIA request with agent assistance"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        agency = Agency.objects.create(
            name='Test Agency',
            slug='test-agency',
            level='federal'
        )
        
        request = FOIARequest.objects.create(
            title='Test Request',
            description='This is a test request',
            user=user,
            agency=agency,
            request_body='I am requesting...',
            status='draft',
            agent_assisted=True,
            agent_improvements='AI suggested improvements'
        )
        
        assert request.agent_assisted
        assert 'improvements' in request.agent_improvements


@pytest.mark.django_db
class TestRequestCommunication:
    """Tests for Request Communication model"""
    
    def test_create_communication(self):
        """Test creating a communication"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        agency = Agency.objects.create(
            name='Test Agency',
            slug='test-agency',
            level='federal'
        )
        
        request = FOIARequest.objects.create(
            title='Test Request',
            description='This is a test request',
            user=user,
            agency=agency,
            request_body='I am requesting...'
        )
        
        comm = RequestCommunication.objects.create(
            request=request,
            direction='outgoing',
            communication_type='email',
            subject='Test Subject',
            content='Test content'
        )
        
        assert comm.request == request
        assert comm.direction == 'outgoing'
        assert comm.communication_type == 'email'
    
    def test_agent_generated_communication(self):
        """Test creating an agent-generated communication"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        agency = Agency.objects.create(
            name='Test Agency',
            slug='test-agency',
            level='federal'
        )
        
        request = FOIARequest.objects.create(
            title='Test Request',
            description='This is a test request',
            user=user,
            agency=agency,
            request_body='I am requesting...'
        )
        
        comm = RequestCommunication.objects.create(
            request=request,
            direction='outgoing',
            communication_type='email',
            subject='Follow-up',
            content='AI generated follow-up',
            agent_generated=True
        )
        
        assert comm.agent_generated
