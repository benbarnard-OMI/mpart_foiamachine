"""
Management command to load Medicaid FOIA contact data from CSV file.
"""
import csv
import re
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.government.models import Government, Nation, Statute
from apps.agency.models import Agency
from apps.contacts.models import Contact, EmailAddress, Phone, Address, Title
from apps.core.models import BaseData

import logging

logger = logging.getLogger('default')

# States that require residency
RESIDENCY_REQUIRED_STATES = [
    'Alabama', 'Arkansas', 'Delaware', 'Georgia', 
    'New Hampshire', 'New Jersey', 'Tennessee', 'Virginia'
]

# Territories
TERRITORIES = [
    'Puerto Rico', 'US Virgin Islands', 'Guam', 
    'American Samoa', 'Northern Mariana Islands'
]

# CMS Regions
CMS_REGIONS = {
    'Puerto Rico': {'region': 'Region 2', 'phone': '(212) 616-2519', 'address': '26 Federal Plaza, New York, NY 10278'},
    'US Virgin Islands': {'region': 'Region 2', 'phone': '(212) 616-2519', 'address': '26 Federal Plaza, New York, NY 10278'},
    'Guam': {'region': 'Region 9', 'phone': '(415) 744-3731', 'address': '90 7th Street, Suite 5-300, San Francisco, CA 94103'},
    'American Samoa': {'region': 'Region 9', 'phone': '(415) 744-3731', 'address': '90 7th Street, Suite 5-300, San Francisco, CA 94103'},
    'Northern Mariana Islands': {'region': 'Region 9', 'phone': '(415) 744-3731', 'address': '90 7th Street, Suite 5-300, San Francisco, CA 94103'},
}


def parse_response_time(response_time_str):
    """
    Parse response time string into days.
    Returns tuple: (days, response_time_type)
    -1 = prompt, -2 = reasonable, -3 = no limit
    """
    if not response_time_str or response_time_str.strip() == '':
        return None, 'none'
    
    response_time_str = response_time_str.strip()
    
    # Check for "prompt"
    if 'prompt' in response_time_str.lower():
        return -1, 'prompt'
    
    # Check for "reasonable"
    if 'reasonable' in response_time_str.lower():
        return -2, 'reasonable'
    
    # Check for "no specific" or "no limit"
    if 'no specific' in response_time_str.lower() or 'no limit' in response_time_str.lower():
        return -3, 'none'
    
    # Try to extract number of days
    match = re.search(r'(\d+)', response_time_str)
    if match:
        days = int(match.group(1))
        return days, 'specific'
    
    # Check for ranges like "10-15 days"
    range_match = re.search(r'(\d+)\s*-\s*(\d+)', response_time_str)
    if range_match:
        # Use the higher number
        days = int(range_match.group(2))
        return days, 'specific'
    
    return None, 'none'


def parse_phone_numbers(phone_str):
    """Parse phone numbers, handling multiple numbers separated by / or comma"""
    if not phone_str or phone_str.strip() == '':
        return []
    
    # Split by / or comma
    phones = re.split(r'[/,]', phone_str)
    return [p.strip() for p in phones if p.strip()]


def parse_name(name_str):
    """Parse name into first_name and last_name"""
    if not name_str or name_str.strip() == '':
        return '', ''
    
    parts = name_str.strip().split()
    if len(parts) == 1:
        return parts[0], ''
    elif len(parts) == 2:
        return parts[0], parts[1]
    else:
        # Assume first is first name, last is last name, middle is everything else
        return parts[0], parts[-1]


def check_residency_required(state_name, legal_notes):
    """Check if residency is required based on state name and legal notes"""
    if state_name in RESIDENCY_REQUIRED_STATES:
        return True
    if legal_notes and 'resident' in legal_notes.lower():
        return True
    return False


def is_territory(state_name):
    """Check if state is a US territory"""
    return state_name in TERRITORIES


class Command(BaseCommand):
    help = 'Load Medicaid FOIA contact data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing Medicaid contact data'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform a dry run without saving to database',
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be saved'))
        
        # Get or create US Nation
        us_nation, created = Nation.objects.get_or_create(
            name='United States',
            defaults={'slug': 'united-states'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created Nation: {us_nation.name}'))
        
        stats = {
            'governments_created': 0,
            'governments_found': 0,
            'agencies_created': 0,
            'agencies_updated': 0,
            'contacts_created': 0,
            'statutes_created': 0,
            'errors': []
        }
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                    try:
                        state_name = row.get('State/Territory', '').strip()
                        if not state_name:
                            continue
                        
                        medicaid_agency_name = row.get('Medicaid Agency Name', '').strip()
                        foia_officer_name = row.get('FOIA Officer Name', '').strip()
                        mailing_address = row.get('Mailing Address', '').strip()
                        phone_number = row.get('Phone Number', '').strip()
                        fax_number = row.get('Fax Number', '').strip()
                        email_address = row.get('Email Address', '').strip()
                        website = row.get('Website', '').strip()
                        submission_methods = row.get('How to Submit Requests', '').strip()
                        response_time = row.get('Statutory Response Time', '').strip()
                        legal_notes = row.get('Legal Considerations & Notes', '').strip()
                        
                        # Determine if territory
                        territory = is_territory(state_name)
                        
                        # Get or create Government (State/Territory)
                        government, gov_created = Government.objects.get_or_create(
                            name=state_name,
                            defaults={
                                'level': '1',  # Admin 1 (State/Province)
                                'nation': us_nation,
                                'slug': state_name.lower().replace(' ', '-')
                            }
                        )
                        
                        if gov_created:
                            stats['governments_created'] += 1
                            self.stdout.write(f'Created Government: {state_name}')
                        else:
                            stats['governments_found'] += 1
                        
                        # Parse response time
                        response_days, response_type = parse_response_time(response_time)
                        
                        # Check residency requirement
                        requires_residency = check_residency_required(state_name, legal_notes)
                        
                        # Get or create Agency
                        agency_name = medicaid_agency_name or f"{state_name} Medicaid Agency"
                        agency, agency_created = Agency.objects.get_or_create(
                            name=agency_name,
                            government=government,
                            defaults={
                                'medicaid_agency_name': medicaid_agency_name,
                                'foia_website': website if website else None,
                                'submission_methods': submission_methods if submission_methods else None,
                                'statutory_response_days': response_days,
                                'requires_residency': requires_residency,
                                'legal_notes': legal_notes if legal_notes else None,
                                'is_territory': territory,
                            }
                        )
                        
                        if not agency_created:
                            # Update existing agency with new data
                            agency.medicaid_agency_name = medicaid_agency_name or agency.medicaid_agency_name
                            agency.foia_website = website if website else agency.foia_website
                            agency.submission_methods = submission_methods if submission_methods else agency.submission_methods
                            agency.statutory_response_days = response_days if response_days else agency.statutory_response_days
                            agency.requires_residency = requires_residency
                            agency.legal_notes = legal_notes if legal_notes else agency.legal_notes
                            agency.is_territory = territory
                            stats['agencies_updated'] += 1
                        else:
                            stats['agencies_created'] += 1
                        
                        # Handle CMS region info for territories
                        if territory and state_name in CMS_REGIONS:
                            cms_info = CMS_REGIONS[state_name]
                            agency.cms_region = cms_info['region']
                            agency.cms_region_contact = f"Phone: {cms_info['phone']}, Address: {cms_info['address']}"
                        
                        if not dry_run:
                            agency.save()
                        
                        # Create FOIA Officer Contact if name provided
                        if foia_officer_name and foia_officer_name.lower() != 'not specified':
                            first_name, last_name = parse_name(foia_officer_name)
                            
                            # Create or get contact
                            contact, contact_created = Contact.objects.get_or_create(
                                first_name=first_name,
                                last_name=last_name,
                                defaults={}
                            )
                            
                            if contact_created:
                                stats['contacts_created'] += 1
                            
                            # Add email
                            if email_address:
                                email_obj, _ = EmailAddress.objects.get_or_create(content=email_address)
                                if email_obj not in contact.emails.all():
                                    contact.emails.add(email_obj)
                                agency.foia_officer_email = email_address
                            
                            # Add phone numbers
                            if phone_number:
                                phones = parse_phone_numbers(phone_number)
                                for phone_str in phones:
                                    phone_obj, _ = Phone.objects.get_or_create(content=phone_str)
                                    if phone_obj not in contact.phone_numbers.all():
                                        contact.phone_numbers.add(phone_obj)
                                agency.foia_officer_phone = phone_number
                            
                            # Add fax
                            if fax_number and fax_number.lower() != 'not specified':
                                fax_obj, _ = Phone.objects.get_or_create(content=fax_number)
                                if fax_obj not in contact.phone_numbers.all():
                                    contact.phone_numbers.add(fax_obj)
                                agency.foia_officer_fax = fax_number
                            
                            # Add address
                            if mailing_address and mailing_address.lower() != 'check dch website':
                                address_obj, _ = Address.objects.get_or_create(content=mailing_address)
                                if address_obj not in contact.addresses.all():
                                    contact.addresses.add(address_obj)
                                agency.foia_mailing_address = mailing_address
                            
                            # Add title if FOIA officer
                            title_obj, _ = Title.objects.get_or_create(content='FOIA Officer')
                            if title_obj not in contact.titles.all():
                                contact.titles.add(title_obj)
                            
                            # Link contact to agency
                            if contact not in agency.contacts.all():
                                agency.contacts.add(contact)
                            
                            agency.foia_officer_name = foia_officer_name
                            
                            if not dry_run:
                                contact.save()
                                agency.save()
                        
                        # Create or update Statute for response time
                        if response_days is not None or response_type != 'none':
                            statute_title = f"{state_name} Public Records Act"
                            statute, statute_created = Statute.objects.get_or_create(
                                short_title=statute_title,
                                defaults={
                                    'days_till_due': response_days if response_days and response_days > 0 else -1,
                                    'response_time_days': response_days if response_days and response_days > 0 else None,
                                    'response_time_type': response_type,
                                    'residency_required': requires_residency,
                                }
                            )
                            
                            if not statute_created:
                                # Update existing statute
                                statute.response_time_days = response_days if response_days and response_days > 0 else statute.response_time_days
                                statute.response_time_type = response_type
                                statute.residency_required = requires_residency
                            
                            # Link statute to government
                            if statute not in government.statutes.all():
                                government.statutes.add(statute)
                            
                            if statute_created:
                                stats['statutes_created'] += 1
                            
                            if not dry_run:
                                statute.save()
                                government.save()
                        
                        self.stdout.write(f'Processed row {row_num}: {state_name} - {agency_name}')
                        
                    except Exception as e:
                        error_msg = f'Error processing row {row_num} ({state_name}): {str(e)}'
                        stats['errors'].append(error_msg)
                        logger.error(error_msg, exc_info=True)
                        self.stdout.write(self.style.ERROR(error_msg))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_file_path}'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading CSV file: {str(e)}'))
            logger.error('Error reading CSV file', exc_info=True)
            return
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Import Summary ==='))
        self.stdout.write(f'Governments created: {stats["governments_created"]}')
        self.stdout.write(f'Governments found: {stats["governments_found"]}')
        self.stdout.write(f'Agencies created: {stats["agencies_created"]}')
        self.stdout.write(f'Agencies updated: {stats["agencies_updated"]}')
        self.stdout.write(f'Contacts created: {stats["contacts_created"]}')
        self.stdout.write(f'Statutes created: {stats["statutes_created"]}')
        
        if stats['errors']:
            self.stdout.write(self.style.WARNING(f'\nErrors encountered: {len(stats["errors"])}'))
            for error in stats['errors'][:10]:  # Show first 10 errors
                self.stdout.write(self.style.ERROR(f'  - {error}'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nDRY RUN - No data was saved'))
