# Teams MCP Server - Claude.ai Connector

A Python MCP server for posting Adaptive Cards to Microsoft Teams and generating email notifications for Jira tickets. Optimized for Claude.ai MCP connector integration.

## 🚀 Claude.ai Setup

### Prerequisites
- Teams webhook URL
- Python 3.9+

### Installation in Claude.ai

1. **Upload to Claude.ai**
   - Upload `teams_mcp_server.py` as MCP connector
   - Set server name: `teams-mcp-server`

2. **Configure Environment**
   - Set `TEAMS_WEBHOOK_URL` with your Teams webhook
   - Set `APPROVAL_EMAIL` for email notifications
   - Set `JIRA_BASE_URL` for Jira integration

3. **Enable Tools**
   - `teams_post_approval_card` - Post approval cards to Teams
   - `teams_build_card_payload` - Generate card payloads
   - `teams_send_approval_email` - Create approval emails

## 🔧 Available Tools

### teams_post_approval_card
Posts an Adaptive Card with Approve/Reject buttons to Teams.

**Required Parameters:**
- `ticket_key`: Jira ticket key (e.g. "TCLOUD-2721")
- `ticket_summary`: Short ticket description
- `user_story`: Full user story text
- `acceptance_criteria`: List of acceptance criteria

**Optional Parameters:**
- `priority`: Priority level (default: "Medium · P2")
- `effort_hours`: Time estimate (default: "2–4 hours")
- `azure_monthly_cost`: Cost estimate (default: "$5–$20 / mo")
- `risk_level`: Risk assessment (default: "Low")
- `labels`: Tags for the ticket (default: ["ai-generated"])
- `webhook_url`: Override default Teams webhook
- `date`: Custom date (default: today)

### teams_build_card_payload
Generates the Adaptive Card JSON without posting to Teams.
Useful for previewing cards or debugging.

### teams_send_approval_email
Generates HTML email for approval notifications.
Returns formatted email ready for manual or programmatic sending.

## 📋 Configuration

### Teams Webhook Setup
1. Go to your Teams channel → "..." → "Connectors"
2. Add "Incoming Webhook"
3. Copy webhook URL to Claude.ai environment settings

### Environment Variables
```
TEAMS_WEBHOOK_URL=https://your-teams-webhook-url
APPROVAL_EMAIL=your-email@company.com
JIRA_BASE_URL=https://your-jira.atlassian.net/browse
```

## 🎯 Usage Examples

### Basic Ticket Approval
```
Post approval card for ticket DEMO-001 with summary "Setup new environment" and user story "As a developer, I need a staging environment" with acceptance criteria ["Environment created", "Access granted"]
```

### Custom Configuration
```
Post approval card for ticket URGENT-123 with high priority and 8-hour effort estimate
```

## ✅ Features

- ✅ **Adaptive Cards**: Rich, interactive approval interface
- ✅ **Action Buttons**: Approve/Reject buttons with ticket data
- ✅ **Email Generation**: HTML email notifications
- ✅ **Input Validation**: Pydantic models ensure data quality
- ✅ **Error Handling**: Graceful failure with clear messages
- ✅ **Claude.ai Ready**: Optimized for MCP connector deployment

## 🔒 Security

- Environment variables for sensitive data
- No credentials stored in code
- HTTPS-only webhook communication
- Input validation prevents injection attacks

---

**Status**: 🟢 Ready for Claude.ai MCP connector deployment
