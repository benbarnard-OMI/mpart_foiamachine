"""
API Views for Agency endpoints using Django REST Framework
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

# Try to import django-filter, but make it optional
try:
    from django_filters.rest_framework import DjangoFilterBackend
    HAS_DJANGO_FILTER = True
except ImportError:
    HAS_DJANGO_FILTER = False

from apps.agency.models import Agency
from apps.agency.serializers import AgencySerializer, MedicaidAgencySerializer
from apps.government.models import Government


class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Agency instances.
    Provides list and detail views for agencies.
    """
    queryset = Agency.objects.all().prefetch_related('government', 'contacts')
    serializer_class = AgencySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    if HAS_DJANGO_FILTER:
        filter_backends.insert(0, DjangoFilterBackend)
        filterset_fields = ['government', 'is_territory', 'requires_residency']
    search_fields = ['name', 'medicaid_agency_name', 'government__name']
    ordering_fields = ['name', 'created', 'statutory_response_days']
    ordering = ['name']
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by state/territory name
        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(government__name__icontains=state)
        
        # Filter by response time
        response_days = self.request.query_params.get('response_days', None)
        if response_days:
            try:
                days = int(response_days)
                queryset = queryset.filter(statutory_response_days=days)
            except ValueError:
                pass
        
        # Filter Medicaid agencies only
        medicaid_only = self.request.query_params.get('medicaid_only', None)
        if medicaid_only and medicaid_only.lower() == 'true':
            queryset = queryset.exclude(medicaid_agency_name__isnull=True).exclude(medicaid_agency_name='')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def medicaid(self, request):
        """
        List all Medicaid agencies with enhanced information
        """
        queryset = self.get_queryset().exclude(
            medicaid_agency_name__isnull=True
        ).exclude(medicaid_agency_name='')
        
        # Apply filters
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MedicaidAgencySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MedicaidAgencySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_state(self, request):
        """
        Get Medicaid agency for a specific state
        Usage: /api/agencies/by_state/?state=California
        """
        state = request.query_params.get('state', None)
        if not state:
            return Response({'error': 'State parameter is required'}, status=400)
        
        try:
            agency = Agency.objects.get(
                government__name__iexact=state,
                medicaid_agency_name__isnull=False
            )
            serializer = MedicaidAgencySerializer(agency)
            return Response(serializer.data)
        except Agency.DoesNotExist:
            return Response({'error': f'Medicaid agency not found for {state}'}, status=404)
        except Agency.MultipleObjectsReturned:
            # If multiple, return the first one
            agency = Agency.objects.filter(
                government__name__iexact=state,
                medicaid_agency_name__isnull=False
            ).first()
            serializer = MedicaidAgencySerializer(agency)
            return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def response_times(self, request):
        """
        Get statistics about response times across all Medicaid agencies
        """
        queryset = self.get_queryset().exclude(
            medicaid_agency_name__isnull=True
        ).exclude(medicaid_agency_name='')
        
        stats = {
            'total_agencies': queryset.count(),
            'by_type': {
                'specific': queryset.exclude(statutory_response_days__lt=0).count(),
                'prompt': queryset.filter(statutory_response_days=-1).count(),
                'reasonable': queryset.filter(statutory_response_days=-2).count(),
                'none': queryset.filter(statutory_response_days__in=[-3, None]).count(),
            },
            'residency_required': queryset.filter(requires_residency=True).count(),
            'territories': queryset.filter(is_territory=True).count(),
            'fastest_response': None,
            'slowest_response': None,
        }
        
        # Find fastest and slowest specific response times
        specific_times = queryset.exclude(statutory_response_days__lt=0).exclude(
            statutory_response_days__isnull=True
        ).order_by('statutory_response_days')
        
        if specific_times.exists():
            fastest = specific_times.first()
            slowest = specific_times.last()
            stats['fastest_response'] = {
                'state': fastest.government.name,
                'days': fastest.statutory_response_days
            }
            stats['slowest_response'] = {
                'state': slowest.government.name,
                'days': slowest.statutory_response_days
            }
        
        return Response(stats)
