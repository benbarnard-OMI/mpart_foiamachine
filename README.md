# MPART FOIA Machine

A customized version of foiamachine for MPART with integrated AI agent flows to reduce administrative burden and improve production efficiency.

## Features

### Core FOIA Management
- Create, track, and manage FOIA requests
- Agency database with contact information
- Document management and tracking
- Communication history tracking
- Status tracking and notifications

### AI Agent Integration (New!)
MPART FOIA Machine includes powerful AI agents that automate repetitive tasks and reduce administrative burden:

1. **Request Drafting Agent** - Automatically drafts professional FOIA requests based on user descriptions
2. **Response Analysis Agent** - Analyzes agency responses and provides actionable insights
3. **Follow-up Agent** - Generates follow-up communications for overdue or incomplete requests
4. **Document Summary Agent** - Summarizes long documents for quick review
5. **Workflow Automation** - Automated task prioritization and processing

### Administrative Improvements
- Automated follow-up generation for overdue requests
- Smart notifications and task prioritization
- Batch processing capabilities
- Reduced manual intervention required
- AI-assisted request quality improvements

## Installation

### Requirements
- Python 3.12+
- PostgreSQL or SQLite (for development)
- Redis (for Celery task queue)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/benbarnard-OMI/mpart_foiamachine.git
cd mpart_foiamachine
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
# Edit .env and add your configuration, especially:
# - SECRET_KEY (generate a new one for production)
# - DATABASE_URL (if using PostgreSQL)
# - OPENAI_API_KEY (for AI agent features)
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. (Optional) Start Celery worker for agent tasks:
```bash
# In a separate terminal
celery -A foiamachine worker -l info

# Start Celery beat for scheduled tasks
celery -A foiamachine beat -l info
```

## Usage

### Basic FOIA Request Flow

1. **Create a Request**
   - Navigate to "Requests" → "Create New"
   - Enter request description
   - Select target agency
   - Use AI agent to draft professional request text (optional)

2. **Submit Request**
   - Review and edit the drafted request
   - Submit to agency via email or portal
   - System tracks submission date and calculates due date

3. **Track Progress**
   - View status on dashboard
   - System automatically checks for overdue requests
   - AI agent suggests follow-ups when needed

4. **Receive Response**
   - Upload or paste agency response
   - AI agent analyzes response and provides summary
   - System suggests next steps (accept, follow-up, appeal)

### AI Agent Features

#### Drafting a Request with AI
```python
# In the UI, click "Use AI Assistant" when creating a request
# Or via API:
POST /api/agents/draft-request/
{
    "description": "I need records related to...",
    "agency_name": "Department of...",
    "agency_type": "federal"
}
```

#### Analyzing a Response
```python
# Click "Analyze with AI" on a received response
# Or via API:
POST /api/agents/analyze-response/{request_id}/
{
    "response_text": "..."
}
```

#### Automated Workflows
The system includes automated workflows that run periodically:
- **Daily at 9 AM**: Check for overdue requests and suggest follow-ups
- **Every 6 hours**: Analyze new responses

## Configuration

### AI Agent Configuration

Edit `.env` to configure AI agents:
```
OPENAI_API_KEY=your-api-key-here
AGENT_MODEL=gpt-4-turbo-preview
AGENT_TEMPERATURE=0.7
```

### Celery Configuration

For production, use Redis as the message broker:
```
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
# Format code
black .

# Lint code
flake8
```

## Architecture

### Apps Structure
- **core** - Base functionality and utilities
- **users** - Custom user model and authentication
- **agency** - Government agency management
- **requests** - FOIA request management (main app)
- **contacts** - Agency contact management
- **agents** - AI agent system (NEW!)
- **mail** - Email handling

### Agent System Architecture

The agent system is built on:
1. **Agent Models** - Track tasks, suggestions, and workflows
2. **Agent Services** - Core business logic for each agent type
3. **Celery Tasks** - Asynchronous processing and scheduled jobs
4. **API Endpoints** - User-facing interfaces for agent features

## Production Deployment

### Heroku
```bash
# Add buildpacks
heroku buildpacks:add heroku/python

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=your-openai-key
heroku config:set DATABASE_URL=your-database-url

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### Docker
(Docker configuration to be added)

## Contributing

This is a customized version for MPART. For contributions:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Create an issue in the repository
- Contact: support@mpartfoia.org

## Acknowledgments

Based on the original [FOIAMachine](https://github.com/cirlabs/foiamachine) by CIR Labs.
Enhanced with AI agent capabilities for MPART.

