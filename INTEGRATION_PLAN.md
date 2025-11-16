# Medicaid FOIA Data Integration Plan

## Overview
This document outlines the integration of comprehensive Medicaid FOIA contact data into the MPART FOIAMachine system.

## Data Files Available

### 1. CSV File: `d49bdec3.csv`
**Content**: Complete contact database for all 50 states + DC + 6 territories (58 total entries)

**Key Fields**:
- State/Territory name
- Medicaid Agency Name
- FOIA Officer Name
- Mailing Address
- Phone Number (often multiple)
- Fax Number
- Email Address
- Website
- How to Submit Requests (submission methods)
- Statutory Response Time (2-30 days or "prompt")
- Legal Considerations & Notes (residency requirements, fees, special procedures)

**Key Observations**:
- 8 states require residency: AL, AR, DE, GA, NH, NJ, TN, VA
- Response times range from 2 days (Vermont) to 30 days (Maryland)
- Territories (PR, USVI, Guam, etc.) may require CMS Regional Office contact
- Submission methods vary: email, online portals, mail, fax

### 2. Legal Guide: `2492f9f5.txt`
**Content**: Comprehensive legal reference covering:
- Federal vs. state FOIA laws
- Response times by state
- Residency requirements
- Procedural requirements (written requests, specificity)
- Fee structures
- Exemptions (HIPAA, trade secrets, etc.)
- Appeals process
- Best practices and examples

### 3. Quick Reference: `93560fbc.txt`
**Content**: Condensed quick-reference guide organized by:
- Response time categories
- Residency restrictions
- Contact methods
- Fee structures
- Decision trees

## Current Codebase Structure

### Django Apps

#### `apps/agency/`
- **Model**: `Agency` - Represents government agencies
  - Fields: name, slug, government (FK), contacts (M2M), creator, hidden
  - Related to: Government, Contact models
- **Purpose**: Manages agency information

#### `apps/contacts/`
- **Model**: `Contact` - Represents individual contacts
  - Fields: first_name, last_name, middle_name, emails (M2M), phone_numbers (M2M), addresses (M2M), titles (M2M)
  - Related models: EmailAddress, Phone, Address, Title
- **Purpose**: Manages contact information for agencies

#### `apps/government/`
- **Model**: `Government` - Represents government entities
  - Fields: name, slug, level (I/S/0/1/2/3), nation (FK), statutes (M2M)
  - Levels: International, Supernational, Admin 0 (National), Admin 1 (State/Province), Admin 2 (County), Admin 3 (City)
- **Model**: `Statute` - Represents FOIA/public records laws
  - Fields: short_title, designator, text, days_till_due, fees_exemptions (M2M)
- **Purpose**: Manages government hierarchy and FOIA statutes

#### `apps/requests/`
- **Purpose**: Manages FOIA requests

#### `apps/mail/`
- **Purpose**: Handles email communications

#### `apps/users/`
- **Purpose**: User management

#### `apps/core/`
- **Purpose**: Core utilities and base models

## Required Changes

### 1. Data Model Enhancements

#### A. Enhance `Agency` Model
**Location**: `foiamachine/apps/agency/models.py`

**New Fields Needed**:
- `medicaid_agency_name` (CharField) - Official Medicaid agency name
- `foia_officer_name` (CharField) - Name of FOIA officer
- `foia_officer_email` (EmailField) - FOIA officer email
- `foia_officer_phone` (CharField) - FOIA officer phone
- `foia_officer_fax` (CharField) - FOIA officer fax
- `foia_mailing_address` (TextField) - Mailing address for FOIA requests
- `foia_website` (URLField) - Agency website
- `submission_methods` (TextField) - How to submit requests (JSON or comma-separated)
- `statutory_response_days` (IntegerField, nullable) - Response time in days (-1 for "prompt")
- `requires_residency` (BooleanField) - Whether state residency is required
- `legal_notes` (TextField) - Special legal considerations
- `is_territory` (BooleanField) - Whether this is a US territory
- `cms_region` (CharField, nullable) - CMS Regional Office if territory
- `cms_region_contact` (TextField, nullable) - CMS Regional Office contact info

#### B. Enhance `Statute` Model
**Location**: `foiamachine/apps/government/models.py`

**New Fields Needed**:
- `response_time_days` (IntegerField) - Specific response time
- `response_time_type` (CharField) - "specific", "prompt", "reasonable", "none"
- `residency_required` (BooleanField) - Whether residency is required
- `fee_structure` (TextField) - Fee information (JSON)
- `exemptions` (TextField) - Common exemptions (JSON)

#### C. Create `MedicaidAgency` Model (Alternative Approach)
**Location**: `foiamachine/apps/agency/models.py` (new model)

**Consideration**: Instead of modifying Agency, create a specialized model that extends or relates to Agency:
- One-to-one relationship with Agency
- Contains all Medicaid-specific fields
- Allows for future expansion to other specialized agency types

### 2. Data Import Script

**Location**: `foiamachine/apps/agency/management/commands/load_medicaid_contacts.py`

**Purpose**: Import CSV data into database

**Steps**:
1. Parse CSV file
2. For each row:
   - Find or create Government (state/territory)
   - Find or create Agency (Medicaid agency)
   - Create/update Contact (FOIA officer)
   - Link Contact to Agency
   - Set all Medicaid-specific fields
   - Create/update Statute with response time info

### 3. API Enhancements

**Location**: `foiamachine/apps/agency/api.py` or `api_urls.py`

**New Endpoints**:
- `/api/medicaid-agencies/` - List all Medicaid agencies
- `/api/medicaid-agencies/{id}/` - Get specific Medicaid agency details
- `/api/medicaid-agencies/by-state/{state}/` - Get Medicaid agency for specific state
- `/api/medicaid-agencies/response-times/` - Get response time statistics

### 4. Admin Interface Updates

**Location**: `foiamachine/apps/agency/admin.py`

**Changes**:
- Add Medicaid-specific fields to admin interface
- Create inline admin for FOIA officer contacts
- Add filters for residency requirements, response times
- Add search by state/territory

### 5. Request Generation Enhancements

**Location**: `foiamachine/apps/requests/`

**Changes**:
- Auto-populate request recipient from Medicaid agency data
- Include response time expectations based on statute
- Warn users about residency requirements
- Include submission method instructions
- Add legal notes to request templates

### 6. UI/View Updates

**Location**: `foiamachine/apps/agency/views.py` and templates

**Changes**:
- Display Medicaid-specific information prominently
- Show response time expectations
- Display residency requirements warnings
- Show submission methods
- Link to legal guide information

## Implementation Steps

### Phase 1: Data Model Updates
1. ✅ Review current models
2. ⬜ Add new fields to Agency model (or create MedicaidAgency model)
3. ⬜ Update Statute model with response time fields
4. ⬜ Create and run migrations

### Phase 2: Data Import
1. ⬜ Create management command to import CSV
2. ⬜ Parse CSV and validate data
3. ⬜ Import into database
4. ⬜ Verify data integrity

### Phase 3: API Updates
1. ⬜ Add new API endpoints
2. ⬜ Update serializers
3. ⬜ Add filtering and search capabilities
4. ⬜ Test API endpoints

### Phase 4: Admin Interface
1. ⬜ Update admin.py
2. ⬜ Add custom admin forms
3. ⬜ Add filters and search
4. ⬜ Test admin interface

### Phase 5: Request Generation
1. ⬜ Update request creation flow
2. ⬜ Add Medicaid-specific fields
3. ⬜ Include legal notes and warnings
4. ⬜ Test request generation

### Phase 6: UI Updates
1. ⬜ Update templates
2. ⬜ Add Medicaid information display
3. ⬜ Add response time tracking
4. ⬜ Test user interface

## Data Mapping

### CSV Column → Model Field Mapping

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

### Special Handling

1. **Residency Requirements**: Parse from Legal Considerations, set `requires_residency` flag
2. **Response Times**: 
   - Parse numeric days (e.g., "10 days" → 10)
   - "Prompt" → -1
   - "Reasonable" → -2
   - "No specific limit" → -3
3. **Territories**: 
   - Set `is_territory = True`
   - Extract CMS region info from notes
4. **Multiple Phone Numbers**: Split by "/" or comma, create multiple Phone objects

## Testing Plan

1. **Unit Tests**: Test model fields and methods
2. **Import Tests**: Test CSV import command
3. **API Tests**: Test new endpoints
4. **Integration Tests**: Test full request flow with Medicaid data
5. **Data Validation**: Verify all 58 entries imported correctly

## Notes

- The original foiamachine codebase uses Django 1.4.8, but the MPART version uses Django 4.2.11
- Need to ensure compatibility with newer Django version
- May need to update model syntax (e.g., ForeignKey requires `on_delete` parameter in newer Django)
- Consider using JSONField for complex data (submission_methods, fee_structure) if using PostgreSQL

## Next Steps

1. Review and approve this plan
2. Start with Phase 1: Data Model Updates
3. Create data import script
4. Test with sample data
5. Full import and verification
