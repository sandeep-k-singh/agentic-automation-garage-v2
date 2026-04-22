---
name: teams-approval-card
description: Converts structured requests into Microsoft Teams Adaptive Cards with Approve/Reject functionality for approval workflows.
version: 1.0.0
---

# Teams Approval Card Skill

## Purpose
Convert a structured request into a Microsoft Teams Adaptive Card with interactive Approve/Reject buttons for approval workflows.

## Responsibilities
- Generate Teams Adaptive Card JSON with approval request details
- Add Action.Submit approve/reject buttons with positive/destructive styling
- Format priority-based visual elements and fact sets
- Include cost estimates and security risk assessments in card layout
- Create webhook-ready Adaptive Card payloads for Teams posting

## Input
The input will usually be JSON from an intake skill, for example:

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

## Your job
Transform the input into a Microsoft Teams Adaptive Card with Approve/Reject functionality.

## Rules
- Create visually clear approval card layout
- Include all key request information
- Display cost and security estimates prominently
- Add interactive Approve/Reject buttons with proper actions
- Include priority-based color coding
- Format acceptance criteria as readable list
- Return JSON only for the adaptive card
- Do not add commentary outside the JSON payload

## Priority Color Mapping
- P1 (Critical): "attention" (red)
- P2 (High): "warning" (yellow/orange)  
- P3 (Medium): "accent" (blue)
- P4 (Low): "good" (green)

## Card Layout Structure
1. **Header**: Title with priority badge
2. **Request Summary**: User story and key details
3. **Cost Information**: Effort and financial estimates
4. **Security Assessment**: Risk level and requirements
5. **Acceptance Criteria**: Formatted list
6. **Action Buttons**: Approve/Reject with callback actions

## Output format
Return JSON only in this adaptive card format:

{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "version": "1.4",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "body": [
          {
            "type": "Container",
            "style": "emphasis",
            "items": [
              {
                "type": "ColumnSet",
                "columns": [
                  {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                      {
                        "type": "TextBlock",
                        "text": "🎯 **Approval Required**",
                        "size": "medium",
                        "weight": "bolder"
                      },
                      {
                        "type": "TextBlock",
                        "text": "${title}",
                        "size": "large",
                        "weight": "bolder",
                        "wrap": true
                      }
                    ]
                  },
                  {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                      {
                        "type": "TextBlock",
                        "text": "${priority}",
                        "size": "small",
                        "weight": "bolder",
                        "color": "${priority_color}",
                        "horizontalAlignment": "right"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "📋 **Request Details**",
                "weight": "bolder",
                "size": "medium"
              },
              {
                "type": "TextBlock",
                "text": "${user_story}",
                "wrap": true,
                "spacing": "small"
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "🎫 **Ticket**: [${ticket_id}](${ticket_url}) | Status: Pending Approval",
                "wrap": true,
                "size": "small",
                "color": "accent"
              }
            ],
            "$when": "${ticket_id != null}"
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "ColumnSet",
                "columns": [
                  {
                    "type": "Column",
                    "width": "50%",
                    "items": [
                      {
                        "type": "TextBlock",
                        "text": "💰 **Cost Estimate**",
                        "weight": "bolder",
                        "size": "medium"
                      },
                      {
                        "type": "TextBlock",
                        "text": "⏱️ Effort: ${effort_hours}",
                        "wrap": true,
                        "size": "small"
                      },
                      {
                        "type": "TextBlock", 
                        "text": "🏗️ Complexity: ${complexity}",
                        "wrap": true,
                        "size": "small"
                      },
                      {
                        "type": "TextBlock",
                        "text": "💵 ${azure_monthly_cost}",
                        "wrap": true,
                        "size": "small"
                      }
                    ]
                  },
                  {
                    "type": "Column",
                    "width": "50%",
                    "items": [
                      {
                        "type": "TextBlock",
                        "text": "🔒 **Security Assessment**",
                        "weight": "bolder",
                        "size": "medium"
                      },
                      {
                        "type": "TextBlock",
                        "text": "⚠️ Risk Level: ${risk_level}",
                        "wrap": true,
                        "size": "small"
                      },
                      {
                        "type": "TextBlock",
                        "text": "🛡️ Requirements: ${security_requirements_text}",
                        "wrap": true,
                        "size": "small"
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "✅ **Acceptance Criteria**",
                "weight": "bolder",
                "size": "medium"
              },
              {
                "type": "TextBlock",
                "text": "${acceptance_criteria_text}",
                "wrap": true,
                "size": "small"
              }
            ]
          },
          {
            "type": "Container",
            "style": "emphasis",
            "items": [
              {
                "type": "TextBlock",
                "text": "👤 **Requested by**: ${requestor}",
                "size": "small"
              },
              {
                "type": "TextBlock", 
                "text": "🆔 **Approval ID**: ${approval_id}",
                "size": "small"
              },
              {
                "type": "TextBlock", 
                "text": "🎫 **Ticket ID**: ${ticket_id}",
                "size": "small",
                "$when": "${ticket_id != null}"
              }
            ]
          }
        ],
        "actions": [
          {
            "type": "Action.Submit",
            "title": "✅ Approve",
            "style": "positive",
            "data": {
              "approval_id": "${approval_id}",
              "ticket_id": "${ticket_id}",
              "action": "approve"
            }
          },
          {
            "type": "Action.Submit", 
            "title": "❌ Reject",
            "style": "destructive",
            "data": {
              "approval_id": "${approval_id}",
              "ticket_id": "${ticket_id}",
              "action": "reject"
            }
          }
        ]
      }
    }
  ]
}

## Variable Substitution Rules
Replace these variables with actual values from input:
- `${title}` → input.title
- `${priority}` → input.priority (display as "Priority: P2")
- `${priority_color}` → mapped color based on priority level
- `${user_story}` → input.user_story
- `${effort_hours}` → input.cost_estimate.effort_hours
- `${complexity}` → input.cost_estimate.complexity
- `${azure_monthly_cost}` → input.cost_estimate.azure_monthly_cost (or service_cost for Halo)
- `${risk_level}` → input.security_estimate.risk_level
- `${security_requirements_text}` → joined security_requirements array
- `${acceptance_criteria_text}` → numbered list from acceptance_criteria array
- `${requestor}` → input.requestor
- `${approval_id}` → input.approval_id
- `${ticket_id}` → input.ticket_id (optional)
- `${ticket_url}` → input.ticket_url (optional)
- `${approval_webhook_url}` → your Teams webhook endpoint

## Acceptance Criteria Formatting
Convert array to numbered text:
```
1. Azure storage account is created in the correct subscription
2. Storage account name follows organisational naming conventions
3. Appropriate redundancy tier is selected
...
```

## Important rules
- Always include approval_id for tracking
- Format security requirements as comma-separated text
- Use priority color mapping consistently
- Include requestor information for accountability
- Set webhook URL to your Teams approval endpoint
- If input missing critical fields, return error message card instead
- Ensure all text wraps properly for mobile display
- Keep card height reasonable (avoid too many acceptance criteria)

## Integration Notes
This card integrates with your existing Teams approval system at:
- Webhook endpoint: `http://orchestrator:7072/api/approvals/{id}/action`
- Expected response: `{ "approval_id": "...", "ticket_id": "...", "action": "approve|reject", "approver": "email" }`