# MPART FOIAMachine

A customized version of [foiamachine](https://github.com/foiamachine/foiamachine) for MPART (Medicaid Public Records Access & Transparency), enhanced with comprehensive Medicaid FOIA contact data integration and modern Django compatibility updates.

## Table of Contents

- [Overview](#overview)
- [Project Strategy](#project-strategy)
- [Key Changes from Original](#key-changes-from-original)
- [Architecture](#architecture)
- [Implementation Status](#implementation-status)
- [Getting Started](#getting-started)
- [Data Import](#data-import)
- [API Usage](#api-usage)
- [Admin Interface](#admin-interface)
- [Technical Details](#technical-details)
- [Future Enhancements](#future-enhancements)

## Overview

This project extends the original foiamachine platform to support Medicaid-specific FOIA (Freedom of Information Act) requests across all 50 US states, the District of Columbia, and 6 US territories. The system provides:

- **Comprehensive Medicaid Agency Database**: Contact information for all 58 state/territory Medicaid agencies
- **FOIA Officer Contacts**: Names, emails, phone numbers, and mailing addresses
- **Response Time Tracking**: Statutory response times by jurisdiction
- **Residency Requirements**: Automatic flagging of states requiring residency
- **Territory Support**: Special handling for US territories with CMS Regional Office information
- **REST API**: Full API access to Medicaid agency data
- **Enhanced Admin Interface**: Streamlined management of Medicaid-specific data

## Project Strategy

### Goals

1. **Data Integration**: Import and manage comprehensive Medicaid FOIA contact data for all US states and territories
2. **Modernization**: Update codebase from Django 1.4.8 to Django 4.2.11 for security and compatibility
3. **API-First Approach**: Provide RESTful API endpoints for programmatic access to Medicaid agency data
4. **User Experience**: Enhance admin and user interfaces with Medicaid-specific information
5. **Request Automation**: Enable automated FOIA request generation with proper legal compliance

### Data Sources

The project integrates data from three key sources:

1. **CSV Database** (`d49bdec3.csv`): Complete contact database for all 58 states/territories including:
   - Medicaid Agency Names
   - FOIA Officer contact information
   - Mailing addresses
   - Phone/fax numbers
   - Email addresses
   - Submission methods
   - Statutory response times
   - Legal considerations and notes

2. **Legal Guide** (`2492f9f5.txt`): Comprehensive legal reference covering:
   - Federal vs. state FOIA laws
   - Response times by state
   - Residency requirements
   - Procedural requirements
   - Fee structures
   - Exemptions
   - Appeals processes

3. **Quick Reference** (`93560fbc.txt`): Condensed guide organized by response times, residency restrictions, contact methods, and fee structures

### Implementation Approach

The integration follows a phased approach:

1. **Data Model Enhancement**: Extend existing models with Medicaid-specific fields
2. **Data Import**: Automated CSV import with validation and error handling
3. **API Development**: RESTful endpoints for data access
4. **Admin Enhancement**: Improved management interface
5. **Request Integration**: Auto-populate FOIA requests with Medicaid data
6. **UI Updates**: User-facing displays of Medicaid information

## Key Changes from Original

### Django Version Upgrade

- **Original**: Django 1.4.8 (Python 2.7)
- **MPART Version**: Django 4.2.11 (Python 3.x)
- **Impact**: Significant compatibility updates required throughout codebase

### Compatibility Updates

1. **ForeignKey Fields**: Added `on_delete` parameters to all ForeignKey fields
2. **Manager Methods**: Changed `get_query_set()` to `get_queryset()` for Django 2.0+ compatibility
3. **String Methods**: Added `__str__` methods alongside `__unicode__` for Python 3 compatibility
4. **ManyToMany Fields**: Removed `null=True` from ManyToManyField definitions

### New Features

1. **Medicaid-Specific Data Model**: Extended Agency model with 13 new fields for Medicaid FOIA data
2. **Enhanced Statute Model**: Added response time tracking, residency requirements, fee structures, and exemptions
3. **Data Import Script**: Automated CSV import command with dry-run support
4. **REST API**: Complete API layer using Django REST Framework
5. **Enhanced Admin**: Improved admin interface with filters, search, and organized fieldsets

### New Apps/Components

- **Government App**: Enhanced with statute improvements and better integration
- **API Layer**: New serializers and viewsets for Agency, Government, Statute, and Contact models

## Architecture

### Django Apps Structure

```
foiamachine/
├── apps/
│   ├── agency/          # Agency management (enhanced with Medicaid fields)
│   ├── contacts/        # Contact information management
│   ├── government/      # Government entities and statutes (enhanced)
│   ├── requests/        # FOIA request management
│   ├── mail/            # Email communications
│   ├── users/           # User management
│   ├── core/            # Core utilities and base models
│   ├── agents/          # AI Agent System
│   └── doccloud/        # Document cloud integration
```

### Data Model Enhancements

#### Agency Model (`foiamachine/apps/agency/models.py`)

**New Medicaid-Specific Fields:**
- `medicaid_agency_name` - Official Medicaid agency name
- `foia_officer_name` - Name of FOIA officer
- `foia_officer_email` - FOIA officer email address
- `foia_officer_phone` - FOIA officer phone number
- `foia_officer_fax` - FOIA officer fax number
- `foia_mailing_address` - Mailing address for FOIA requests
- `foia_website` - Agency website for FOIA information
- `submission_methods` - How to submit requests (JSON or text)
- `statutory_response_days` - Response time in days (-1 for prompt, -2 for reasonable, -3 for no limit)
- `requires_residency` - Boolean flag for residency requirements
- `legal_notes` - Special legal considerations
- `is_territory` - Boolean flag for US territories
- `cms_region` - CMS Regional Office if territory
- `cms_region_contact` - CMS Regional Office contact information

#### Statute Model (`foiamachine/apps/government/models.py`)

**Enhanced Fields:**
- `response_time_days` - Specific response time in days
- `response_time_type` - Type of response time (specific, prompt, reasonable, none)
- `residency_required` - Boolean flag for residency requirements
- `fee_structure` - Fee information in JSON format
- `exemptions` - Common exemptions in JSON format

### Data Relationships

```
Government (State/Territory)
    ↓ (ForeignKey)
Agency (Medicaid Agency)
    ↓ (ManyToMany)
Contact (FOIA Officer)
    ↓ (ManyToMany)
EmailAddress, Phone, Address, Title

Government
    ↓ (ManyToMany)
Statute (FOIA Law)
```

## Implementation Status

### ✅ Completed

#### 1. Data Model Updates
- ✅ Added 13 Medicaid-specific fields to Agency model
- ✅ Enhanced Statute model with response time and residency fields
- ✅ Updated all ForeignKey fields with `on_delete` parameters
- ✅ Fixed manager methods for Django 2.0+ compatibility
- ✅ Added `__str__` methods for Python 3 compatibility
- ✅ Created database migrations

#### 2. Data Import Script
- ✅ Created `load_medicaid_contacts.py` management command
- ✅ CSV parsing with validation
- ✅ Automatic Government entity creation/updates
- ✅ Automatic Agency entity creation/updates
- ✅ Contact entity creation and linking
- ✅ Response time parsing (handles "prompt", "reasonable", numeric days, ranges)
- ✅ Residency requirement detection
- ✅ Territory CMS region handling
- ✅ Dry-run mode for testing
- ✅ Detailed import statistics

#### 3. API Endpoints
- ✅ REST API using Django REST Framework
- ✅ Serializers for Agency, Government, Statute, Contact
- ✅ ViewSet with custom actions
- ✅ URL routing configured
- ✅ Endpoints:
  - `GET /api/agencies/` - List all agencies (with filtering)
  - `GET /api/agencies/{id}/` - Get specific agency details
  - `GET /api/agencies/medicaid/` - List all Medicaid agencies with enhanced info
  - `GET /api/agencies/by_state/?state=California` - Get Medicaid agency for specific state
  - `GET /api/agencies/response_times/` - Get response time statistics
- ✅ Filtering by government, is_territory, requires_residency
- ✅ Search by name, medicaid_agency_name, government name
- ✅ Ordering by name, created date, response days

#### 4. Admin Interface
- ✅ Enhanced list display with Medicaid fields
- ✅ List filters for territory, residency, government, response time
- ✅ Search across multiple fields including Medicaid-specific fields
- ✅ Organized fieldsets:
  - Basic Information
  - Medicaid Agency Information
  - FOIA Officer Contact
  - Submission & Response
  - Territory Information (collapsed)
  - Contacts (collapsed)
  - Statistics (collapsed)
- ✅ Custom response time display with color coding
- ✅ Optimized queryset with prefetch_related

#### 5. Settings Configuration
- ✅ Added `foiamachine.apps.government` to INSTALLED_APPS
- ✅ API URL patterns configured

### ⬜ Future Enhancements

#### 6. Request Generation Integration
- ⬜ Update `foiamachine/apps/requests/models.py` to reference Medicaid fields
- ⬜ Auto-populate recipient from Medicaid agency data
- ⬜ Include response time expectations
- ⬜ Add residency requirement warnings
- ⬜ Include submission method instructions

#### 7. UI/View Updates
- ⬜ Update `foiamachine/apps/agency/views.py`
- ⬜ Create/update templates to show:
  - Response time expectations
  - Residency requirements warnings
  - Submission methods
  - Legal notes
  - CMS region info for territories

## Getting Started

### Prerequisites

- Python 3.x
- Django 4.2.11
- PostgreSQL (recommended) or SQLite (for development)
- Django REST Framework

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mpart_foiamachine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings**
   - Update `foiamachine/config/settings.py` or use environment-specific settings
   - Configure database connection
   - Set up static files and media storage

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Data Import

### Importing Medicaid Contact Data

The system includes a management command to import Medicaid FOIA contact data from CSV:

```bash
# Standard import
python manage.py load_medicaid_contacts d49bdec3.csv

# Dry-run mode (preview without saving)
python manage.py load_medicaid_contacts d49bdec3.csv --dry-run
```

### Import Process

The import script performs the following operations:

1. **Parses CSV file** with all 58 states/territories
2. **Creates or updates Government entities** (states/territories)
3. **Creates or updates Agency entities** with Medicaid-specific data
4. **Creates Contact entities** for FOIA officers
5. **Links contacts to agencies** via ManyToMany relationships
6. **Parses response times** (handles "prompt", "reasonable", numeric days, ranges)
7. **Detects residency requirements** from legal notes
8. **Handles territories** with CMS region information
9. **Provides detailed statistics** on import results

### Data Coverage

The implementation supports all 58 entries from the CSV:
- 50 US States
- District of Columbia
- 6 US Territories (Puerto Rico, USVI, Guam, American Samoa, Northern Mariana Islands)

**Special Handling:**
- 8 states with residency requirements automatically flagged (AL, AR, DE, GA, NH, NJ, TN, VA)
- Territories linked to CMS Regional Offices
- Response times parsed and categorized (specific, prompt, reasonable, none)
- Multiple phone numbers supported (split by "/" or comma)
- Missing data handled gracefully

### Data Mapping

| CSV Column | Model Field | Model | Notes |
|------------|-------------|-------|-------|
| State/Territory | name | Government | Find or create |
| Medicaid Agency Name | name | Agency | Find or create |
| FOIA Officer Name | first_name, last_name | Contact | Split if possible |
| Mailing Address | addresses | Contact | Add to Contact |
| Phone Number | phone_numbers | Contact | Add to Contact |
| Fax Number | phone_numbers | Contact | Add with type "fax" |
| Email Address | emails | Contact | Add to Contact |
| Website | foia_website | Agency | New field |
| How to Submit Requests | submission_methods | Agency | New field |
| Statutory Response Time | statutory_response_days | Agency | Parse days or -1 for "prompt" |
| Legal Considerations & Notes | legal_notes | Agency | New field |

### Response Time Parsing

The import script handles various response time formats:
- **Numeric days**: "10 days" → 10
- **Prompt**: "prompt" → -1
- **Reasonable**: "reasonable" → -2
- **No specific limit**: "no limit" → -3
- **Ranges**: "5-10 days" → 10 (uses maximum)

## API Usage

### Base URL

All API endpoints are prefixed with `/api/`

### Endpoints

#### List All Agencies
```bash
GET /api/agencies/
```

**Query Parameters:**
- `government` - Filter by government ID
- `is_territory` - Filter by territory status (true/false)
- `requires_residency` - Filter by residency requirement (true/false)
- `search` - Search by name, medicaid_agency_name, or government name
- `ordering` - Order by: name, created, response_days

**Example:**
```bash
curl http://localhost:8000/api/agencies/?search=California&ordering=name
```

#### Get Specific Agency
```bash
GET /api/agencies/{id}/
```

**Example:**
```bash
curl http://localhost:8000/api/agencies/1/
```

#### List Medicaid Agencies
```bash
GET /api/agencies/medicaid/
```

Returns all agencies with enhanced Medicaid-specific information.

**Example:**
```bash
curl http://localhost:8000/api/agencies/medicaid/
```

#### Get Agency by State
```bash
GET /api/agencies/by_state/?state=California
```

**Example:**
```bash
curl http://localhost:8000/api/agencies/by_state/?state=California
```

#### Response Time Statistics
```bash
GET /api/agencies/response_times/
```

Returns statistics about response times across all agencies.

**Example:**
```bash
curl http://localhost:8000/api/agencies/response_times/
```

### Response Format

All endpoints return JSON responses. Example agency response:

```json
{
  "id": 1,
  "name": "California Department of Health Care Services",
  "medicaid_agency_name": "California Department of Health Care Services",
  "foia_officer_name": "John Doe",
  "foia_officer_email": "foia@dhcs.ca.gov",
  "foia_officer_phone": "(916) 555-1234",
  "foia_mailing_address": "1501 Capitol Avenue, Sacramento, CA 95814",
  "statutory_response_days": 10,
  "requires_residency": false,
  "is_territory": false,
  "government": {
    "id": 1,
    "name": "California",
    "level": "1"
  }
}
```

## Admin Interface

### Accessing Admin

Navigate to `/admin/agency/agency/` to view and manage Medicaid agencies.

### Features

- **Enhanced List Display**: Shows key Medicaid fields at a glance
- **Advanced Filtering**: Filter by territory, residency requirements, government, response time
- **Search**: Search across name, Medicaid agency name, government name, and contact fields
- **Organized Fieldsets**: Information grouped logically:
  - Basic Information
  - Medicaid Agency Information
  - FOIA Officer Contact
  - Submission & Response
  - Territory Information (collapsed)
  - Contacts (collapsed)
  - Statistics (collapsed)
- **Response Time Display**: Color-coded display for quick identification
- **Optimized Performance**: Uses prefetch_related for efficient queries

### Custom Admin Actions

The admin interface includes custom actions for bulk operations on agencies.

## Technical Details

### Django Version Compatibility

- **Updated for**: Django 4.2.11 (from original Django 1.4.8)
- **Python Version**: Python 3.x (from Python 2.7)
- **Key Updates**:
  - All ForeignKey fields include `on_delete` parameters
  - Manager methods use `get_queryset()` instead of `get_query_set()`
  - Added `__str__` methods for Python 3 compatibility
  - Updated ManyToManyField definitions (removed null=True)

### Dependencies

- Django 4.2.11
- Django REST Framework (for API)
- django-filter (optional, for advanced filtering)
- PostgreSQL (recommended) or SQLite (for development)

### Database

- Supports PostgreSQL (recommended) and SQLite (for development)
- Migrations are reversible
- All new fields are nullable or have defaults to support existing data

### Files Modified/Created

#### Modified Files:
1. `foiamachine/apps/agency/models.py` - Added Medicaid fields
2. `foiamachine/apps/government/models.py` - Enhanced Statute model
3. `foiamachine/apps/agency/admin.py` - Enhanced admin interface
4. `foiamachine/apps/agency/api_urls.py` - Added API routing
5. `foiamachine/config/settings.py` - Added government app
6. `foiamachine/config/urls.py` - Added API URL pattern

#### New Files:
1. `foiamachine/apps/agency/management/commands/load_medicaid_contacts.py` - Import script
2. `foiamachine/apps/agency/serializers.py` - API serializers
3. `foiamachine/apps/agency/api_views.py` - API views
4. `foiamachine/apps/agency/migrations/0003_add_medicaid_fields.py` - Migration
5. `foiamachine/apps/government/migrations/0002_add_statute_enhancements.py` - Migration

### Testing Checklist

- [ ] Run migrations successfully
- [ ] Import CSV data without errors
- [ ] Verify all 58 entries imported
- [ ] Test API endpoints
- [ ] Test admin interface
- [ ] Verify response time parsing
- [ ] Verify residency requirement detection
- [ ] Verify territory CMS region linking
- [ ] Test filtering and search
- [ ] Verify data relationships (Agency -> Government -> Statute)

## Future Enhancements

### Request Generation Integration

To integrate Medicaid data into request generation:

1. Update `foiamachine/apps/requests/models.py` to reference Medicaid fields
2. Auto-populate recipient from Medicaid agency data
3. Include response time expectations
4. Add residency requirement warnings
5. Include submission method instructions

### UI/View Updates

To display Medicaid information in views:

1. Update `foiamachine/apps/agency/views.py`
2. Create/update templates to show:
   - Response time expectations
   - Residency requirements warnings
   - Submission methods
   - Legal notes
   - CMS region info for territories

### Additional Features

- **Request Tracking**: Track FOIA requests against statutory response times
- **Automated Reminders**: Send reminders based on response time deadlines
- **Legal Guide Integration**: Link to legal guide information in templates
- **Bulk Operations**: Admin actions for bulk updates
- **Export Functionality**: Export agency data to CSV/JSON
- **Analytics Dashboard**: Response time statistics and compliance metrics

## License

MIT License - See LICENSE file for details.

## Contributing

This is a customized version for MPART. For contributions or questions, please contact the project maintainers.

## Support

For issues or questions related to:
- **Original foiamachine**: See [foiamachine repository](https://github.com/foiamachine/foiamachine)
- **MPART customization**: Contact project maintainers
