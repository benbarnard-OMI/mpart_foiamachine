# FOIAMachine Automation Opportunities

This document identifies opportunities for API enhancements, webhooks, and agent flows to reduce human involvement in the FOIA request management process.

## Executive Summary

FOIAMachine currently requires significant manual intervention for:
- Request status updates
- Email thread association
- Response interpretation
- Follow-up actions
- Data extraction from responses

This document outlines specific opportunities to automate these processes through enhanced APIs, webhook integrations, and intelligent agent flows.

---

## Current Architecture Overview

### Key Components
- **Request Management**: Django models for FOIA requests with status tracking
- **Email Handling**: Mailgun integration for sending/receiving emails
- **Contact Management**: Database of government contacts and agencies
- **Status Tracking**: Manual status updates (New, Filed, Response Received, Partially Fulfilled, Fulfilled, Denied)
- **Notifications**: Scheduled commands for overdue requests and sunset notifications

### Current API Endpoints (Tastypie)
- `/api/v1/request/` - CRUD operations for requests
- `/api/v1/contact/` - Contact management
- `/api/v1/agency/` - Agency information
- `/api/v1/mail/` - Message resources
- `/api/v1/agencystats/` - Agency statistics
- `/api/v1/userstats/` - User statistics

---

## 1. API ENHANCEMENTS

### 1.1 Request Creation API Enhancements

**Current State**: 
- Basic POST to `/api/v1/request/` exists
- Requires manual contact selection
- Manual agency/government selection

**Opportunities**:

#### 1.1.1 Bulk Request Creation API
```python
POST /api/v1/request/bulk/
{
  "template": {
    "text": "Request text",
    "title": "Request title",
    "record_types": ["meeting minutes"],
    "acceptable_responses": ["PDF", "CSV"]
  },
  "agencies": [1, 2, 3],  # Agency IDs
  "contacts": [10, 11, 12]  # Optional: specific contacts
}
```
**Benefit**: Create multiple requests at once, reducing repetitive manual work

#### 1.1.2 Smart Agency/Contact Resolution API
```python
POST /api/v1/request/smart-create/
{
  "text": "Request for police department records",
  "government": "California",
  "agency_name": "Los Angeles Police Department",  # Fuzzy match
  "auto_select_contact": true  # Auto-select best contact
}
```
**Benefit**: Reduces manual lookup and selection steps

#### 1.1.3 Request Template API
```python
GET /api/v1/request/templates/
POST /api/v1/request/templates/
POST /api/v1/request/from-template/{template_id}/
```
**Benefit**: Standardize common request types, enable programmatic reuse

### 1.2 Status Management API

**Current State**: 
- Status updates require manual API calls
- No programmatic status transitions

**Opportunities**:

#### 1.2.1 Batch Status Update API
```python
PATCH /api/v1/request/batch-update/
{
  "request_ids": [1, 2, 3],
  "status": "Fulfilled",
  "date_fulfilled": "2024-01-15"
}
```
**Benefit**: Update multiple requests at once

#### 1.2.2 Status Transition Validation API
```python
POST /api/v1/request/{id}/transition/
{
  "to_status": "Fulfilled",
  "validate": true  # Check if transition is valid
}
```
**Benefit**: Ensure status transitions follow business rules

### 1.3 Email Thread Management API

**Current State**: 
- Manual association of orphaned messages
- Thread lookup relies on regex patterns

**Opportunities**:

#### 1.3.1 Enhanced Thread Association API
```python
POST /api/v1/mail/associate-thread/
{
  "message_id": 123,
  "request_id": 456,
  "confidence": "high"  # For ML-based suggestions
}
```

#### 1.3.2 Bulk Thread Association API
```python
POST /api/v1/mail/bulk-associate/
{
  "associations": [
    {"message_id": 1, "request_id": 10},
    {"message_id": 2, "request_id": 11}
  ]
}
```
**Benefit**: Reduce manual clicking through orphaned messages

---

## 2. WEBHOOK INTEGRATIONS

### 2.1 Request Lifecycle Webhooks

**Opportunities**:

#### 2.1.1 Request Status Change Webhook
```python
POST {external_url}/webhooks/request-status-changed
{
  "request_id": 123,
  "old_status": "Filed",
  "new_status": "Response Received",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_url": "https://foiamachine.org/requests/123/"
}
```
**Use Cases**:
- External monitoring systems
- Analytics dashboards
- Notification services
- Integration with other tools

#### 2.1.2 Request Created Webhook
```python
POST {external_url}/webhooks/request-created
{
  "request_id": 123,
  "agency": "FBI",
  "government": "United States of America",
  "author": "user@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 2.1.3 Request Due Date Approaching Webhook
```python
POST {external_url}/webhooks/request-due-soon
{
  "request_id": 123,
  "due_date": "2024-01-20T00:00:00Z",
  "days_remaining": 5,
  "agency": "FBI"
}
```
**Benefit**: Proactive notifications before manual cron jobs run

### 2.2 Email Event Webhooks

**Current State**: 
- Mailgun webhook exists at `/mail/incoming/`
- Only handles incoming messages

**Opportunities**:

#### 2.2.1 Email Sent Confirmation Webhook
```python
POST {external_url}/webhooks/email-sent
{
  "request_id": 123,
  "message_id": 456,
  "recipients": ["foia@agency.gov"],
  "sent_at": "2024-01-15T10:30:00Z",
  "mailgun_message_id": "abc123"
}
```

#### 2.2.2 Email Delivery Status Webhook
```python
POST {external_url}/webhooks/email-delivered
POST {external_url}/webhooks/email-bounced
POST {external_url}/webhooks/email-failed
```
**Benefit**: Track delivery issues automatically, update request status

#### 2.2.3 Response Received Webhook
```python
POST {external_url}/webhooks/response-received
{
  "request_id": 123,
  "message_id": 456,
  "from": "foia@agency.gov",
  "subject": "RE: FOIA Request",
  "has_attachments": true,
  "attachment_count": 3,
  "received_at": "2024-01-15T10:30:00Z"
}
```
**Benefit**: Trigger automated processing workflows

### 2.3 Contact/Agency Update Webhooks

**Opportunities**:

#### 2.3.1 Contact Information Updated Webhook
```python
POST {external_url}/webhooks/contact-updated
{
  "contact_id": 123,
  "agency_id": 456,
  "changes": {
    "email": {"old": "old@agency.gov", "new": "new@agency.gov"},
    "title": {"old": "FOIA Officer", "new": "Senior FOIA Officer"}
  }
}
```

---

## 3. AGENT FLOWS (AI/ML Automation)

### 3.1 Intelligent Email Processing

**Current State**: 
- Manual email parsing
- Manual thread association
- Manual status updates

**Opportunities**:

#### 3.1.1 Auto-Status Detection Agent

**Flow**:
1. Incoming email received → Webhook triggered
2. Agent analyzes email content:
   - Keywords: "fulfilled", "denied", "partial", "appeal"
   - Sentiment analysis
   - Attachment presence/type
   - Response patterns
3. Agent suggests status update:
   ```python
   POST /api/v1/request/{id}/suggest-status/
   {
     "suggested_status": "Partially Fulfilled",
     "confidence": 0.85,
     "reasoning": "Email mentions 'partial release' and contains attachments",
     "auto_apply": false  # User confirmation required
   }
   ```
4. User confirms or overrides
5. Status updated automatically

**Implementation Points**:
- `apps/mail/models.py` - `MailMessage.parse_message_http()` - Add ML analysis
- `apps/requests/models.py` - `Request.set_status()` - Add auto-detection hook

**Benefit**: Reduces manual status updates by 60-80%

#### 3.1.2 Auto-Thread Association Agent

**Flow**:
1. Orphaned message detected
2. Agent analyzes:
   - Subject line patterns
   - Email headers (References, In-Reply-To)
   - Sender email domain
   - Content similarity to existing requests
   - Thread lookup codes in body/subject
3. Agent suggests associations:
   ```python
   GET /api/v1/mail/orphaned/suggestions/
   Response: {
     "message_id": 123,
     "suggestions": [
       {
         "request_id": 456,
         "confidence": 0.92,
         "reason": "Subject line matches, sender domain matches agency"
       }
     ]
   }
   ```
4. Auto-associate high-confidence matches (>0.95)
5. Queue medium-confidence for review

**Implementation Points**:
- `apps/mail/models.py` - `MailBox.lookup_thread()` - Enhance with ML
- `apps/mail/views.py` - `associate_message()` - Add bulk auto-association

**Benefit**: Eliminates 70-90% of manual thread association work

#### 3.1.3 Response Content Extraction Agent

**Flow**:
1. Response email received with attachments
2. Agent extracts:
   - Document metadata (dates, page counts)
   - Key information (exemptions cited, fees charged)
   - Redaction patterns
   - Responsive vs non-responsive indicators
3. Agent creates structured data:
   ```python
   POST /api/v1/request/{id}/extracted-data/
   {
     "exemptions_cited": ["Exemption 5", "Exemption 7(C)"],
     "pages_released": 150,
     "pages_withheld": 50,
     "fees_charged": 25.00,
     "response_type": "partial",
     "appeal_deadline": "2024-02-15"
   }
   ```
4. Auto-populate request fields
5. Generate summary for user

**Implementation Points**:
- New module: `apps/requests/agents/content_extractor.py`
- Integration with document parsing (PDF, DOCX)

**Benefit**: Automates data entry, improves accuracy

### 3.2 Intelligent Request Management

#### 3.2.1 Auto-Follow-Up Agent

**Flow**:
1. Request overdue detected (existing: `notify_overdue_requests.py`)
2. Agent analyzes:
   - Previous communication patterns
   - Agency response history
   - Request complexity
3. Agent generates follow-up email:
   ```python
   POST /api/v1/request/{id}/generate-followup/
   {
     "tone": "professional",
     "urgency": "moderate",
     "include_appeal_info": true,
     "suggested_text": "Generated follow-up email..."
   }
   ```
4. User reviews and sends
5. Schedule next follow-up automatically

**Implementation Points**:
- Enhance `apps/requests/management/commands/notify_overdue_requests.py`
- Add email template generation

**Benefit**: Reduces time spent crafting follow-ups

#### 3.2.2 Request Optimization Agent

**Flow**:
1. User drafts request
2. Agent analyzes:
   - Similar successful requests
   - Agency-specific preferences
   - Legal requirements
3. Agent suggests improvements:
   ```python
   POST /api/v1/request/{id}/suggest-improvements/
   {
     "suggestions": [
       {
         "type": "clarity",
         "text": "Consider specifying date range more precisely",
         "original": "recent records",
         "suggested": "records from January 1, 2020 to December 31, 2023"
       },
       {
         "type": "format",
         "text": "This agency prefers CSV format",
         "suggested_format": "CSV"
       }
     ]
   }
   ```

**Benefit**: Improves request success rates

#### 3.2.3 Contact Discovery Agent

**Flow**:
1. User selects agency
2. Agent searches:
   - Recent successful requests to same agency
   - Contact update patterns
   - Public FOIA logs
3. Agent suggests best contact:
   ```python
   GET /api/v1/agency/{id}/suggest-contact/
   Response: {
     "contact_id": 123,
     "confidence": 0.88,
     "reason": "Used in 15 successful requests in last 6 months",
     "response_rate": 0.92
   }
   ```

**Benefit**: Reduces manual contact research

### 3.3 Predictive Analytics Agent

#### 3.3.1 Response Time Prediction

**Flow**:
1. Request created
2. Agent analyzes:
   - Historical agency response times
   - Request complexity
   - Current agency workload
   - Time of year (holidays, fiscal year end)
3. Agent predicts:
   ```python
   GET /api/v1/request/{id}/predictions/
   Response: {
     "predicted_response_days": 25,
     "confidence_interval": [18, 32],
     "factors": {
       "agency_avg": 22,
       "complexity_penalty": 3,
       "seasonal_adjustment": 0
     }
   }
   ```

**Benefit**: Set realistic expectations, improve planning

#### 3.3.2 Success Probability Prediction

**Flow**:
1. Request drafted
2. Agent predicts fulfillment probability:
   ```python
   POST /api/v1/request/{id}/predict-success/
   Response: {
     "fulfillment_probability": 0.72,
     "partial_probability": 0.18,
     "denial_probability": 0.10,
     "recommendations": [
       "Consider narrowing date range to improve success rate",
       "This agency has high denial rate for similar requests"
     ]
   }
   ```

**Benefit**: Guide users to improve requests before sending

---

## 4. INTEGRATION OPPORTUNITIES

### 4.1 External Service Integrations

#### 4.1.1 Document Cloud Integration Enhancement
**Current**: Basic integration exists
**Opportunity**: 
- Auto-upload responses to DocumentCloud
- Auto-extract text for searchability
- Auto-tag documents with request metadata
- Webhook: `POST /webhooks/documentcloud-processed`

#### 4.1.2 Calendar Integration
**Opportunity**:
- Auto-create calendar events for due dates
- Send reminders via calendar apps
- Sync appeal deadlines
- Webhook: `POST /webhooks/calendar-sync`

#### 4.1.3 Slack/Teams Integration
**Opportunity**:
- Notify teams of status changes
- Share request updates in channels
- Webhook: `POST /webhooks/slack-notification`

#### 4.1.4 Legal Research Integration
**Opportunity**:
- Auto-cite relevant statutes
- Suggest legal precedents
- Check exemption validity
- API: `GET /api/v1/request/{id}/legal-research/`

### 4.2 Government Portal Integrations

#### 4.2.1 FOIA.gov Integration
**Opportunity**:
- Sync requests with FOIA.gov submissions
- Track federal request status
- Webhook: `POST /webhooks/foia-gov-update`

#### 4.2.2 State Portal Integrations
**Opportunity**:
- Integrate with state-specific FOIA portals
- Auto-submit to portals
- Track status across systems

---

## 5. IMPLEMENTATION PRIORITY

### Phase 1: High-Impact, Low-Effort (Quick Wins)
1. **Batch Status Update API** - Simple endpoint addition
2. **Request Status Change Webhook** - Event emission on status updates
3. **Auto-Thread Association (High Confidence)** - Simple rule-based matching
4. **Response Received Webhook** - Enhance existing email handler

**Estimated Impact**: 30-40% reduction in manual work

### Phase 2: Medium-Impact, Medium-Effort
1. **Auto-Status Detection Agent** - ML model for status classification
2. **Bulk Request Creation API** - Template-based creation
3. **Contact Discovery Agent** - Historical analysis
4. **Enhanced Thread Association** - ML-based matching

**Estimated Impact**: Additional 25-35% reduction in manual work

### Phase 3: High-Impact, High-Effort (Strategic)
1. **Response Content Extraction Agent** - Document parsing + NLP
2. **Request Optimization Agent** - ML-based suggestions
3. **Predictive Analytics** - Historical data analysis
4. **External Integrations** - Third-party service connections

**Estimated Impact**: Additional 20-30% reduction, plus quality improvements

---

## 6. TECHNICAL IMPLEMENTATION NOTES

### 6.1 Code Locations for Key Enhancements

#### Request Status Updates
- **File**: `foiamachine/apps/requests/models.py`
- **Method**: `Request.set_status()` (line 188)
- **Enhancement**: Add webhook emission, validation logic

#### Email Processing
- **File**: `foiamachine/apps/mail/models.py`
- **Method**: `MailBox.parse_message_http()` (line 309)
- **Enhancement**: Add ML analysis, auto-status detection

#### Thread Association
- **File**: `foiamachine/apps/mail/models.py`
- **Method**: `MailBox.lookup_thread()` (line 420)
- **Enhancement**: Improve matching algorithm, add confidence scoring

#### Webhook Infrastructure
- **New File**: `foiamachine/apps/core/webhooks.py`
- **Purpose**: Centralized webhook emission system
- **Integration**: Django signals for event emission

#### Agent Infrastructure
- **New Directory**: `foiamachine/apps/agents/`
- **Files**:
  - `status_detector.py` - Status classification
  - `thread_matcher.py` - Thread association
  - `content_extractor.py` - Document analysis
  - `predictor.py` - Response time/success prediction

### 6.2 Database Schema Additions

```sql
-- Webhook subscriptions
CREATE TABLE webhook_subscriptions (
    id INT PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(50),
    webhook_url TEXT,
    secret_key VARCHAR(255),
    active BOOLEAN
);

-- Agent suggestions (for user review)
CREATE TABLE agent_suggestions (
    id INT PRIMARY KEY,
    request_id INT,
    suggestion_type VARCHAR(50),
    suggested_value TEXT,
    confidence FLOAT,
    applied BOOLEAN,
    created_at TIMESTAMP
);

-- Request predictions
CREATE TABLE request_predictions (
    id INT PRIMARY KEY,
    request_id INT,
    predicted_response_days INT,
    fulfillment_probability FLOAT,
    created_at TIMESTAMP
);
```

### 6.3 API Rate Limiting Considerations

- Webhook endpoints: Implement exponential backoff
- Agent endpoints: Queue-based processing for heavy operations
- Batch operations: Limit batch sizes (e.g., max 100 requests)

---

## 7. METRICS FOR SUCCESS

### Key Performance Indicators
1. **Manual Status Updates**: Target 70% reduction
2. **Thread Association Time**: Target 80% reduction
3. **Request Creation Time**: Target 50% reduction
4. **Response Processing Time**: Target 60% reduction
5. **User Satisfaction**: Measure via surveys

### Monitoring
- Track webhook delivery success rates
- Monitor agent suggestion acceptance rates
- Measure API usage patterns
- Track error rates for automated processes

---

## 8. SECURITY CONSIDERATIONS

### API Security
- Implement OAuth 2.0 for API access
- Rate limiting per user/IP
- Webhook signature verification
- Input validation and sanitization

### Agent Security
- User confirmation for high-impact actions
- Audit logs for all automated changes
- Confidence thresholds for auto-application
- Rollback mechanisms for incorrect actions

---

## 9. CONCLUSION

The FOIAMachine platform has significant opportunities for automation through:
1. **Enhanced APIs** for programmatic access and bulk operations
2. **Webhooks** for real-time event notifications and integrations
3. **Agent Flows** for intelligent automation of repetitive tasks

Implementing these enhancements in phases will progressively reduce manual work while maintaining system reliability and user control. The highest-impact opportunities are in email processing automation and status management, which currently require the most manual intervention.

---

## APPENDIX: Current Manual Processes Inventory

### High-Frequency Manual Tasks
1. **Status Updates**: Users manually update request status when responses arrive
2. **Thread Association**: Users manually link orphaned emails to requests
3. **Contact Selection**: Users manually browse and select contacts
4. **Request Drafting**: Users manually compose request text
5. **Follow-up Emails**: Users manually craft and send follow-ups

### Medium-Frequency Manual Tasks
1. **Agency Selection**: Users manually search and select agencies
2. **Attachment Management**: Users manually upload and associate attachments
3. **Group Sharing**: Users manually share requests with groups
4. **Tag Management**: Users manually tag requests for organization

### Low-Frequency Manual Tasks
1. **Contact Updates**: Users manually update contact information
2. **Agency Creation**: Users manually create new agencies
3. **Report Generation**: Users manually generate statistics reports

---

*Document generated: 2024-01-15*
*Based on analysis of FOIAMachine codebase from https://github.com/cirlabs/foiamachine*
