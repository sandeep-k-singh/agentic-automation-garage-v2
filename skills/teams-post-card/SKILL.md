---
name: teams-post-card
description: Posts an adaptive card to a Microsoft Teams channel using incoming webhooks
version: 1.0.0
---

# Teams Post Card Skill

## Purpose
Post a Microsoft Teams Adaptive Card to a specific channel using incoming webhook functionality.

## Responsibilities
- Post Adaptive Card JSON payloads to Teams channels via incoming webhooks
- Handle Teams webhook URL configuration and authentication
- Validate Adaptive Card structure before posting
- Return success/failure status with posting confirmation
- Manage Teams API integration and error handling

## Input
The input should be JSON containing the adaptive card and channel information:

{
  "webhook_url": "https://clearchannelint.webhook.office.com/webhookb2/eefeea19-a884-453f-862f-9b990ea5763b@1623e08b-aca1-49c6-b577-89c5bd4aa7b4/IncomingWebhook/9a1e2caf6bb940ac9829939638697dd9/f2c771bb-566e-48b5-91ae-d077c9e81035/V28x-tIx4FYXndxqW1eQ3jW9wWXkD4u_5xsdeo7rI2mDE1",
  "adaptive_card": {
    "type": "message",
    "attachments": [
      {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": { ... }
      }
    ]
  },
  "channel_info": {
    "name": "General",
    "team": "Clear Channel"
  }
}

## Your job
Post the adaptive card to the specified Teams channel and return success/failure status.

## Rules
- Use HTTP POST to the webhook URL
- Send the adaptive_card JSON as the request body
- Set Content-Type header to application/json
- Handle webhook response codes appropriately
- Return clear success/failure status
- Include error details if posting fails
- Validate webhook URL format before posting
- Add retry logic for transient failures

## Webhook URL Validation
- Must start with https://outlook.office.com/webhook/ OR https://{tenant}.webhook.office.com/webhookb2/
- Must contain valid webhook token
- Should be HTTPS only for security
- Teams webhook URLs are tenant-specific (e.g., clearchannelint.webhook.office.com)

## Output format
Return JSON status with details:

Success response:
{
  "status": "success",
  "message": "Card posted successfully to Teams channel",
  "channel": "General",
  "team": "Clear Channel",
  "posted_at": "2026-04-21T10:30:00Z",
  "webhook_response_code": 200
}

Failure response:
{
  "status": "error", 
  "error_type": "webhook_failure",
  "message": "Failed to post card to Teams channel",
  "error_details": "HTTP 400: Bad Request - Invalid card format",
  "channel": "General",
  "team": "Clear Channel",
  "attempted_at": "2026-04-21T10:30:00Z",
  "troubleshooting": "Check adaptive card format and webhook URL validity"
}

## Error Handling
- **Invalid webhook URL**: Return validation error
- **HTTP 400**: Bad card format - check adaptive card JSON structure
- **HTTP 401/403**: Webhook unauthorized - verify webhook is still active
- **HTTP 429**: Rate limited - implement retry with backoff
- **HTTP 500**: Teams service error - retry after delay
- **Network timeout**: Connection issue - retry up to 3 times

## Integration Notes
- Works with Teams incoming webhooks (easiest setup)
- Requires webhook URL configuration per channel
- Supports standard Teams adaptive card format with Action.Submit buttons
- Can be chained after teams-approval-card skill  
- Handles webhook authentication automatically via URL
- Compatible with Action.Submit interactive elements for user responses

## Usage Example
```javascript
// 1. Generate approval card
const approvalCard = await generateTeamsApprovalCard(requestData);

// 2. Post to Teams channel  
const postResult = await postTeamsCard({
  webhook_url: process.env.TEAMS_APPROVALS_WEBHOOK,
  adaptive_card: approvalCard,
  channel_info: {
    name: "Approvals",
    team: "IT Operations" 
  }
});

// 3. Handle result
if (postResult.status === "success") {
  console.log("Approval card posted to Teams");
} else {
  console.error("Failed to post card:", postResult.error_details);
}
```

## Environment Configuration
Recommended environment variables:
- `TEAMS_GENERAL_WEBHOOK` - General channel webhook
- `TEAMS_APPROVALS_WEBHOOK` - Approvals channel webhook  
- `TEAMS_URGENT_WEBHOOK` - Urgent requests channel webhook
- `TEAMS_INFRASTRUCTURE_WEBHOOK` - Infrastructure team channel webhook

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
- Validate card content before posting
- Log posting activity for audit purposes