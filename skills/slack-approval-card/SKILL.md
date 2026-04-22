---
name: slack-approval-card
description: Converts structured requests into Slack Block Kit messages with interactive Approve/Reject buttons for approval workflows.
version: 1.0.0
---

# Slack Approval Card Skill

## Purpose
Convert a structured request into a Slack Block Kit message with interactive Approve/Reject buttons for approval workflows.

## Input
The input will usually be JSON from an intake skill, for example:

```json
{
  "route": "jira",
  "needs_clarification": false,
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
  "labels": ["ai-generated", "slack-intake", "azure", "storage", "infrastructure"],
  "cost_estimate": {
    "effort_hours": "2-4 hours",
    "complexity": "Medium",
    "dependencies": ["Azure subscription access", "Resource group permissions"],
    "azure_monthly_cost": "Estimated monthly cost: $10-25 (assumptions: Standard LRS, 500GB storage, moderate operations)"
  },
  "security_estimate": {
    "risk_level": "Medium",
    "security_requirements": ["RBAC controls", "Private endpoints", "Audit logging"],
    "compliance_impact": "Data residency requirements for demo environment"
  },
  "requestor": "john.doe@company.com",
  "approval_id": "APPR-2024-001",
  "ticket_id": "CLOUDREQ-1234",
  "ticket_url": "https://company.atlassian.net/browse/CLOUDREQ-1234"
}
```

## Your job
Transform the input into a Slack Block Kit message with Approve/Reject functionality.

## Rules
- Create visually clear approval card layout using Slack Block Kit
- Include all key request information
- Display cost and security estimates prominently
- Add interactive Approve/Reject buttons with proper actions
- Include priority-based emoji indicators
- Format acceptance criteria as readable list using mrkdwn
- Return JSON only for the Slack message payload
- Do not add commentary outside the JSON payload

## Priority Emoji Mapping
- P1 (Critical): 🔴 (red circle)
- P2 (High): 🟡 (yellow circle)  
- P3 (Medium): 🔵 (blue circle)
- P4 (Low): 🟢 (green circle)

## Card Layout Structure
1. **Header Section**: Title with priority indicator and approval badge
2. **Request Details**: User story and key information
3. **Cost Information**: Effort and financial estimates in fields
4. **Security Assessment**: Risk level and requirements
5. **Acceptance Criteria**: Formatted as bullet list
6. **Action Buttons**: Approve (Primary) / Reject (Danger) with callback IDs

## Output format
Return JSON only in this Slack Block Kit format:

```json
{
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
        "text": "*${priority_emoji} ${priority} | ${title}*"
      },
      "accessory": {
        "type": "button",
        "text": {
          "type": "plain_text",
          "text": "View Ticket"
        },
        "url": "${ticket_url}",
        "action_id": "view_ticket"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*📋 Request Details*\n${user_story}"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*💰 Effort & Cost*\n${effort_hours}\n${azure_monthly_cost}"
        },
        {
          "type": "mrkdwn", 
          "text": "*🔒 Security Risk*\n${risk_level}\n${security_requirements}"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*✅ Acceptance Criteria*\n${formatted_criteria}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*📊 Labels*\n`${labels_text}`"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "✅ Approve"
          },
          "style": "primary",
          "action_id": "approve_request",
          "value": "${approval_id}"
        },
        {
          "type": "button", 
          "text": {
            "type": "plain_text",
            "text": "❌ Reject"
          },
          "style": "danger",
          "action_id": "reject_request",
          "value": "${approval_id}"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Requested by: ${requestor} | ID: ${approval_id} | Ticket: <${ticket_url}|${ticket_id}>"
        }
      ]
    }
  ]
}
```

## Variable Substitution Rules
- `${title}` → Request title
- `${priority}` → Priority level (P1, P2, etc.)
- `${priority_emoji}` → Emoji based on priority mapping
- `${user_story}` → Full user story text
- `${effort_hours}` → Effort estimate from cost_estimate.effort_hours
- `${azure_monthly_cost}` → Azure cost from cost_estimate.azure_monthly_cost
- `${risk_level}` → Security risk level from security_estimate.risk_level
- `${security_requirements}` → Formatted security requirements list
- `${formatted_criteria}` → Acceptance criteria formatted as bullet points with • prefix
- `${labels_text}` → Labels joined with spaces
- `${approval_id}` → Unique approval ID for tracking
- `${ticket_id}` → Jira ticket key
- `${ticket_url}` → Direct link to Jira ticket
- `${requestor}` → Email of person making request

## Interactive Components
- **View Ticket Button**: Opens Jira ticket in browser
- **Approve Button**: Primary style, action_id "approve_request", value is approval_id
- **Reject Button**: Danger style, action_id "reject_request", value is approval_id

Both approval buttons should include the approval_id as the value for tracking responses.