"""
Serializers for Agency API endpoints
"""
from rest_framework import serializers
from apps.agency.models import Agency
from apps.government.models import Government, Statute
from apps.contacts.models import Contact


class GovernmentSerializer(serializers.ModelSerializer):
    """Serializer for Government model"""
    class Meta:
        model = Government
        fields = ['id', 'name', 'slug', 'level']


class StatuteSerializer(serializers.ModelSerializer):
    """Serializer for Statute model"""
    class Meta:
        model = Statute
        fields = ['id', 'short_title', 'days_till_due', 'response_time_days', 
                  'response_time_type', 'residency_required']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model"""
    emails = serializers.SerializerMethodField()
    phone_numbers = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'emails', 'phone_numbers', 'addresses']
    
    def get_emails(self, obj):
        return [email.content for email in obj.get_active_emails()]
    
    def get_phone_numbers(self, obj):
        return [phone.content for phone in obj.get_active_phones()]
    
    def get_addresses(self, obj):
        return [addr.content for addr in obj.get_active_addressess()]


class AgencySerializer(serializers.ModelSerializer):
    """Serializer for Agency model"""
    government = GovernmentSerializer(read_only=True)
    contacts = ContactSerializer(many=True, read_only=True)
    statutes = serializers.SerializerMethodField()
    
    class Meta:
        model = Agency
        fields = [
            'id', 'name', 'slug', 'government', 'contacts',
            'medicaid_agency_name', 'foia_officer_name', 'foia_officer_email',
            'foia_officer_phone', 'foia_officer_fax', 'foia_mailing_address',
            'foia_website', 'submission_methods', 'statutory_response_days',
            'requires_residency', 'legal_notes', 'is_territory', 'cms_region',
            'cms_region_contact', 'statutes', 'created', 'pub_contact_cnt'
        ]
        read_only_fields = ['id', 'slug', 'created', 'pub_contact_cnt']
    
    def get_statutes(self, obj):
        """Get statutes associated with the agency's government"""
        if obj.government:
            statutes = obj.government.statutes.all()
            return StatuteSerializer(statutes, many=True).data
        return []


class MedicaidAgencySerializer(serializers.ModelSerializer):
    """Specialized serializer for Medicaid agencies with enhanced fields"""
    government = GovernmentSerializer(read_only=True)
    primary_contact = serializers.SerializerMethodField()
    response_time_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Agency
        fields = [
            'id', 'name', 'slug', 'government', 'medicaid_agency_name',
            'foia_officer_name', 'foia_officer_email', 'foia_officer_phone',
            'foia_officer_fax', 'foia_mailing_address', 'foia_website',
            'submission_methods', 'statutory_response_days', 'requires_residency',
            'legal_notes', 'is_territory', 'cms_region', 'cms_region_contact',
            'primary_contact', 'response_time_info'
        ]
    
    def get_primary_contact(self, obj):
        """Get primary FOIA officer contact information"""
        if obj.foia_officer_name:
            return {
                'name': obj.foia_officer_name,
                'email': obj.foia_officer_email,
                'phone': obj.foia_officer_phone,
                'fax': obj.foia_officer_fax,
                'address': obj.foia_mailing_address,
            }
        return None
    
    def get_response_time_info(self, obj):
        """Get formatted response time information"""
        if obj.statutory_response_days is None:
            return {'type': 'none', 'days': None, 'description': 'No specific limit'}
        
        if obj.statutory_response_days == -1:
            return {'type': 'prompt', 'days': None, 'description': 'Prompt response required'}
        elif obj.statutory_response_days == -2:
            return {'type': 'reasonable', 'days': None, 'description': 'Reasonable time'}
        elif obj.statutory_response_days == -3:
            return {'type': 'none', 'days': None, 'description': 'No specific limit'}
        else:
            return {
                'type': 'specific',
                'days': obj.statutory_response_days,
                'description': f'{obj.statutory_response_days} business days'
            }
