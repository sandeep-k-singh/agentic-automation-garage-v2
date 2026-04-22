---
name: slack-approval-workflow  
description: Complete workflow skill that generates Slack Block Kit approval cards and posts them to Slack channels using webhooks or bot tokens
version: 2.0.0
---

# Slack Approval Workflow Skill

## Purpose
Orchestrate the complete Slack approval workflow: generate approval card + post to Slack channel in one skill.

## Responsibilities
- Execute complete Slack approval workflow from start to finish
- Generate approval cards using slack-approval-card skill integration
- Post messages to designated Slack channels via slack-post-card skill
- Manage webhook URLs and channel configuration
- Coordinate approval workflow completion and response handling

## Input
The input should be the structured request data plus Slack configuration:

```json
{
  "route": "jira",
  "title": "Create Azure storage account for demo environment", 
  "user_story": "As a demo team member, I want an Azure storage account provisioned in the demo environment so that I can store and access application data needed for demonstrations.",
  "acceptance_criteria": [
    "Azure storage account is created in the correct subscription and resource group for the demo environment",
    "Storage account name follows organisational naming conventions",
    "Appropriate redundancy tier is selected",
    "Access is restricted to approved users and services",
    "Storage account is tagged with environment, owner, and cost centre tags",
    "Soft delete and basic diagnostic logging is enabled"
  ],
  "priority": "P2",
  "labels": ["ai-generated", "slack-intake", "azure", "storage"],
  "cost_estimate": {
    "effort_hours": "2-4 hours",
    "complexity": "Medium", 
    "azure_monthly_cost": "Estimated monthly cost: $15-30"
  },
  "security_estimate": {
    "risk_level": "Medium",
    "security_requirements": ["RBAC controls", "Private endpoints", "Audit logging"]
  },
  "requestor": "john.doe@company.com",
  "approval_id": "APPR-2026-045",
  "ticket_id": "CLOUDREQ-1234",
  "ticket_url": "https://company.atlassian.net/browse/CLOUDREQ-1234",
  "slack_config": {
      "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    "channel": "#approvals",
    "bot_token": "xoxb-xxxxxxxxx-xxxxxxxxx-xxxxxxxxxxxx",
    "method": "webhook"
  }
}
```

## Your job
1. Generate Slack approval card using slack-approval-card skill
2. Post the card to Slack channel using webhook or bot API
3. Return comprehensive workflow status with message details

## Rules
- Chain both card generation and posting in sequence
- Pass request data to slack-approval-card skill first
- Take generated Block Kit message and post to Slack
- Support both webhook and bot token posting methods
- Handle failures at each step gracefully
- Return comprehensive workflow status
- Include card generation AND posting results
- Provide clear error messages for troubleshooting
- Include Slack message timestamp and channel for reference

## Slack Posting Methods
### Method 1: Webhook (Preferred for simple posting)
- Use `webhook_url` from slack_config
- POST the Block Kit JSON directly to webhook
- No authentication headers needed
- Simpler but less control over message options

### Method 2: Bot Token (For advanced features)  
- Use `bot_token` from slack_config
- POST to `https://slack.com/api/chat.postMessage`
- Include `Authorization: Bearer {bot_token}` header
- More control and message metadata available

## Channel Routing Logic
Route approval messages based on:
- **Priority**: P1 requests → Post to #critical-approvals + mention @channel
- **Labels**: 
  - Infrastructure requests → Post to #infrastructure-approvals
  - Security requests → Post to #security-approvals  
  - Default → Post to #general-approvals
- **Cost**: High cost requests (>$100/mo) → CC finance team channel

## Output Format
Return comprehensive workflow status:

```json
{
  "workflow_status": "success",
  "approval_id": "APPR-2026-045",
  "steps": {
    "card_generation": {
      "status": "success",
      "timestamp": "2026-04-22T10:30:00Z",
      "card_blocks_count": 8,
      "card_size_bytes": 2847
    },
    "slack_posting": {
      "status": "success", 
      "timestamp": "2026-04-22T10:30:01Z",
      "method": "webhook",
      "channel": "#approvals",
      "message_ts": "1713780601.123456",
      "permalink": "https://workspace.slack.com/archives/C1234567890/p1713780601123456"
    }
  },
  "message_details": {
    "channel": "#approvals",
    "message_ts": "1713780601.123456", 
    "permalink": "https://workspace.slack.com/archives/C1234567890/p1713780601123456",
    "blocks_posted": 8,
    "interactive_elements": ["approve_button", "reject_button", "view_ticket_button"]
  },
  "next_steps": [
    "Monitor channel for approval responses",
    "Update Jira ticket when decision is made", 
    "Notify requestor of outcome"
  ],
  "troubleshooting": {
    "webhook_test_url": "https://hooks.slack.com/services/...",
    "channel_verification": "Confirm bot is member of target channel",
    "permissions_check": "Verify chat:write scope for bot token"
  }
}
```

## Error Handling
Handle common Slack posting errors:

- **Invalid webhook**: Return clear error with webhook validation steps
- **Channel not found**: Suggest channel verification and bot membership
- **Permission denied**: Guide through bot scopes and workspace permissions  
- **Rate limiting**: Provide retry guidance and backoff strategy
- **Message too large**: Suggest content truncation strategies

## Interactive Button Handling
The posted message will include interactive buttons that need webhook endpoints to handle:

- **Approve button**: action_id "approve_request" 
- **Reject button**: action_id "reject_request"
- **View ticket button**: Opens Jira ticket URL

Provide guidance on setting up interactive webhook endpoints to handle these button clicks.

## Security Considerations
- Never log or expose bot tokens in output
- Mask webhook URLs in logs (show only domain)
- Validate all input parameters before posting
- Sanitize user-provided text content for Slack formatting
- Rate limit posting to prevent spam

## Slack Block Kit Validation
Validate the generated Block Kit before posting:
- Maximum 50 blocks per message
- Text blocks under 3000 characters
- Valid action_id format for interactive elements
- Proper mrkdwn formatting syntax
- Required fields present in all block types

Return validation errors if Block Kit is malformed before attempting to post.