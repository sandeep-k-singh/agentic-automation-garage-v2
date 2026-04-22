---
name: slack-post-card
description: Posts a Block Kit message to a Slack channel using webhooks or bot tokens
version: 1.0.0
---

# Slack Post Card Skill

## Purpose
Post a Slack Block Kit message to a specific channel using incoming webhook or bot token functionality.

## Input
The input should be JSON containing the Block Kit message and channel information:

```json
{
  \"webhook_url\": \"https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK\",
  "bot_token": "xoxb-xxxxxxxxx-xxxxxxxxx-xxxxxxxxxxxx",
  "method": "webhook",
  "block_kit_message": {
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "🎯 Approval Required"
        }
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Create Azure storage account for demo environment*"
        }
      }
    ]
  },
  "channel_info": {
    "channel": "#approvals",
    "workspace": "ClearChannel"
  }
}
```

## Your job
Post the Block Kit message to the specified Slack channel and return success/failure status with message details.

## Rules
- Support both webhook and bot token posting methods
- Use HTTP POST to appropriate Slack API endpoint
- Send the block_kit_message JSON as the request body
- Set proper Content-Type and Authorization headers
- Handle Slack API response codes appropriately
- Return clear success/failure status with message timestamp
- Include error details if posting fails
- Validate webhook URL or bot token format before posting
- Add retry logic for transient failures

## Posting Methods

### Method 1: Webhook (Preferred for simple posting)
- Use `webhook_url` from input
- POST Block Kit JSON directly to webhook
- Endpoint: The provided webhook URL
- Headers: `Content-Type: application/json`
- No authentication headers needed
- Simpler but less control over message options

### Method 2: Bot Token (For advanced features)  
- Use `bot_token` from input
- POST to `https://slack.com/api/chat.postMessage`
- Headers: `Authorization: Bearer {bot_token}`, `Content-Type: application/json`
- Include channel in request body
- More control and message metadata available

## Webhook URL Validation
- Must start with `https://hooks.slack.com/services/`
- Must contain valid webhook token path (T.../B.../...)
- Should be HTTPS only for security
- Slack webhook URLs are workspace-specific

## Bot Token Validation
- Must start with `xoxb-` for bot tokens
- Must contain proper token format
- Requires appropriate scopes (chat:write minimum)

## Output format
Return JSON status with details:

**Success response:**
```json
{
  "status": "success",
  "message": "Block Kit message posted successfully to Slack channel",
  "channel": "#approvals",
  "workspace": "ClearChannel", 
  "method": "webhook",
  "posted_at": "2026-04-22T10:30:00Z",
  "message_ts": "1713780600.123456",
  "permalink": "https://workspace.slack.com/archives/C1234567890/p1713780600123456",
  "blocks_posted": 8,
  "interactive_elements": ["approve_button", "reject_button"]
}
```

**Failure response:**
```json
{
  "status": "error", 
  "error_type": "api_failure",
  "message": "Failed to post Block Kit message to Slack channel",
  "error_details": "invalid_blocks: Block validation failed",
  "channel": "#approvals",
  "workspace": "ClearChannel",
  "method": "webhook",
  "attempted_at": "2026-04-22T10:30:00Z",
  "troubleshooting": "Check Block Kit format and webhook URL validity"
}
```

## Error Handling

### Webhook Errors
- **Invalid webhook URL**: Return validation error
- **invalid_payload**: Bad Block Kit format - check blocks JSON structure
- **channel_not_found**: Webhook channel deleted or moved
- **Rate limited**: Implement retry with exponential backoff
- **Network timeout**: Connection issue - retry up to 3 times

### Bot Token Errors  
- **invalid_auth**: Bot token invalid or expired
- **missing_scope**: Bot needs chat:write scope
- **channel_not_found**: Channel doesn't exist or bot not member
- **not_in_channel**: Bot needs to join channel first
- **Rate limited**: Respect Slack rate limits

## Block Kit Validation
Validate Block Kit before posting:
- Maximum 50 blocks per message
- Text blocks under 3000 characters
- Valid block types (section, header, divider, actions, etc.)
- Proper mrkdwn formatting syntax
- Required fields present in all block types
- Interactive elements have valid action_ids

## Integration Notes
- Works with Slack incoming webhooks (easiest setup)
- Supports bot tokens for advanced features
- Requires webhook URL or bot token configuration
- Supports standard Slack Block Kit format
- Can be chained after slack-approval-card skill
- Handles Slack authentication automatically

## Channel Routing
Support different posting strategies based on content:
- **Priority channels**: Route urgent approvals to specific channels
- **Team channels**: Route by labels or request type
- **Default channel**: Fallback for general approvals
- **Cross-posting**: Post to multiple channels for high-priority items

## Usage Example
```javascript
// 1. Generate approval card
const approvalCard = await generateSlackApprovalCard(requestData);

// 2. Post to Slack channel  
const postResult = await postSlackCard({
  webhook_url: process.env.SLACK_APPROVALS_WEBHOOK,
  block_kit_message: approvalCard,
  method: "webhook",
  channel_info: {
    channel: "#approvals",
    workspace: "ClearChannel"
  }
});

if (postResult.status === "success") {
  console.log(`Posted to ${postResult.channel} at ${postResult.posted_at}`);
  console.log(`Message link: ${postResult.permalink}`);
}
```

## Security Considerations
- Never log bot tokens in plaintext
- Mask webhook URLs in logs (show only domain)
- Validate all input parameters before posting
- Sanitize user content for Slack mrkdwn formatting
- Rate limit posting to prevent spam
- Store tokens securely in environment variables

## Interactive Button Setup
If Block Kit includes interactive elements:
- Configure interactive webhook endpoint in Slack app settings
- Handle button clicks with action_ids
- Verify request signatures from Slack
- Respond to interactions within 3 seconds
- Update original message or send ephemeral responses