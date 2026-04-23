---
name: teams-posting-bot
description: Post a response to Slack or Teams channel with created Jira or Halo ticket confirmation
version: 1.0.0
---

# Teams Posting Bot Skill

## Purpose
Post ticket confirmation messages to Slack or Teams channels after a Jira or Halo ticket is successfully created. Formats ticket data appropriately for each platform and notifies requestors and approvers with actionable ticket links.

## Responsibilities
- Post ticket creation confirmations to Slack channels
- Post ticket creation confirmations to Teams channels
- Format ticket data for Jira vs Halo requests
- Handle platform-specific card/message formatting
- Return success/failure status with posting confirmation
- Manage webhook URL configuration and authentication
- Validate message structure before posting

## Input
The input should be JSON containing ticket data and channel information:

For Slack:
```json
{
  "platform": "slack",
  "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "ticket_data": {
    "ticket_id": "PROJ-123",
    "ticket_system": "jira",
    "title": "Create Azure storage account",
    "requestor": "john.doe@company.com",
    "priority": "P2",
    "ticket_url": "https://jira.company.com/browse/PROJ-123"
  },
  "channel_info": {
    "name": "#hackathon4-approval",
    "team": "IT Operations"
  }
}
```

For Teams:
```json
{
  "platform": "teams",
  "webhook_url": "https://clearchannelint.webhook.office.com/webhookb2/...",
  "ticket_data": {
    "ticket_id": "HALO-456",
    "ticket_system": "halo",
    "title": "Grant database access",
    "requestor": "jane.smith@company.com",
    "priority": "P3",
    "ticket_url": "https://halo.company.com/tickets/456"
  },
  "channel_info": {
    "name": "IT Requests",
    "team": "Clear Channel"
  }
}
```

## Your Job
1. Validate ticket data and webhook URL
2. Format message appropriately for platform (Slack Block Kit or Teams Adaptive Card)
3. Post to the specified channel via webhook
4. Return success/failure status with confirmation

## Rules
- Use HTTP POST to the webhook URL
- Set Content-Type header to application/json
- Support both Jira and Halo ticket systems
- Include ticket ID, title, priority, and link in message
- Add visual indicators (emoji/colors) for priority levels
- Handle platform-specific formatting requirements
- Return clear success/failure status
- Include error details if posting fails
- Validate webhook URL format before posting
- Implement retry logic for transient failures

## Platform-Specific Formatting

### Slack Format
- Use Block Kit formatting
- Include ticket ID as header
- Show priority with emoji indicators (P1=🚨, P2=⚠️, P3=ℹ️, P4=💡)
- Add action button with ticket link
- Include requestor info in context block
- Color code by ticket system (blue for Jira, green for Halo)

### Teams Format
- Use Adaptive Card format
- Include ticket ID and system badge
- Show priority with color indicators
- Add "View Ticket" action button
- Include requestor and creation timestamp
- Format based on ticket system (different styles for Jira vs Halo)

## Priority Indicators
- P1 (Critical): 🚨 Red/Critical styling
- P2 (High): ⚠️ Orange/High styling  
- P3 (Normal): ℹ️ Blue/Normal styling
- P4 (Low): 💡 Gray/Low styling

## Output Format
Return JSON status with details:

Success response:
```json
{
  "status": "success",
  "message": "Ticket confirmation posted successfully",
  "platform": "slack",
  "ticket_id": "PROJ-123",
  "ticket_system": "jira",
  "channel": "#hackathon4-approval",
  "posted_at": "2026-04-21T10:30:00Z",
  "webhook_response_code": 200
}
```

Failure response:
```json
{
  "status": "error",
  "error_type": "posting_failure",
  "message": "Failed to post ticket confirmation",
  "error_details": "HTTP 400: Invalid webhook URL format",
  "ticket_id": "PROJ-123",
  "channel": "#hackathon4-approval",
  "attempted_at": "2026-04-21T10:30:00Z",
  "troubleshooting": "Verify webhook URL is valid and contains authentication token"
}
```

## Error Handling
- **Invalid webhook URL**: Return validation error
- **Missing ticket data**: Return missing fields error
- **HTTP 400**: Bad message format - check block/card JSON structure
- **HTTP 401/403**: Webhook unauthorized - verify webhook is still active
- **HTTP 429**: Rate limited - implement retry with backoff
- **HTTP 500**: Platform service error - retry after delay
- **Network timeout**: Connection issue - retry up to 3 times
- **Unknown platform**: Return error specifying supported platforms (slack, teams)

## Integration Notes
- Works with Slack incoming webhooks
- Works with Teams incoming webhooks
- Automatically formats based on ticket system (Jira vs Halo)
- Can be chained after ticket-intake-router skill
- Requires webhook URL configuration per channel
- Handles webhook authentication automatically via URL
- Supports both direct URLs and webhook token lookup

## Usage Example
```javascript
// 1. Generate Jira ticket in ticket-intake-router
const ticketResult = await createJiraTicket(requestData);

// 2. Post confirmation to Slack approval channel
const slackPost = await postTicketConfirmation({
  platform: "slack",
  webhook_url: process.env.SLACK_APPROVALS_WEBHOOK,
  ticket_data: {
    ticket_id: ticketResult.key,
    ticket_system: "jira",
    title: ticketResult.fields.summary,
    requestor: ticketResult.fields.reporterEmail,
    priority: ticketResult.fields.priority.name,
    ticket_url: ticketResult.key // Will append Jira base URL
  },
  channel_info: {
    name: "#hackathon4-approval",
    team: "IT Operations"
  }
});

// 3. Handle result
if (slackPost.status === "success") {
  console.log("Ticket confirmation posted to Slack");
} else {
  console.error("Failed to post:", slackPost.error_details);
}
```

## Environment Configuration
Recommended environment variables:
- `SLACK_APPROVALS_WEBHOOK` - Slack approvals channel webhook
- `SLACK_NOTIFICATIONS_WEBHOOK` - Slack notifications channel webhook
- `TEAMS_APPROVALS_WEBHOOK` - Teams approvals channel webhook
- `TEAMS_NOTIFICATIONS_WEBHOOK` - Teams notifications channel webhook
- `JIRA_BASE_URL` - Base URL for Jira ticket links
- `HALO_BASE_URL` - Base URL for Halo ticket links

## Retry Logic
- Retry on 5xx errors (server issues)
- Retry on network timeouts
- Exponential backoff: 1s, 2s, 4s
- Maximum 3 retry attempts
- Don't retry on 4xx errors (client issues)

## Security Considerations
- Webhook URLs contain authentication tokens
- Store webhook URLs securely (environment variables)
- Use HTTPS webhooks only
- Validate ticket data before posting
- Sanitize requestor information for display
- Log posting activity for audit purposes
- Never log full webhook URLs with tokens

## Ticket System Custom Formatting

### Jira Tickets
- Badge: "Jira"
- Color scheme: Blue/professional
- Link format: `{JIRA_BASE_URL}/browse/{ticket_id}`
- Include custom fields if available
- Show story points if available

### Halo Tickets
- Badge: "Halo"  
- Color scheme: Green/supportive
- Link format: `{HALO_BASE_URL}/tickets/{ticket_id}`
- Include SLA information if available
- Show assigned team if available